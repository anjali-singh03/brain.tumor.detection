import os
import numpy as np
import tensorflow as tf
from PIL import Image
import streamlit as st

from src.utils import get_logger
from src.config import INPUT_SHAPE, MODEL_PATH

logger = get_logger(__name__)


def _generate_jet_lut() -> np.ndarray:
    """Generate 256-entry RGB JET colormap lookup table using pure NumPy."""
    x = np.linspace(0.0, 1.0, 256)
    r = np.clip(np.minimum(4.0 * x - 1.5, -4.0 * x + 4.5), 0.0, 1.0)
    g = np.clip(np.minimum(4.0 * x - 0.5, -4.0 * x + 3.5), 0.0, 1.0)
    b = np.clip(np.minimum(4.0 * x + 0.5, -4.0 * x + 2.5), 0.0, 1.0)
    return np.uint8(255 * np.stack([r, g, b], axis=-1))


_JET_LUT = _generate_jet_lut()


@st.cache_resource
def load_model(model_path: str = None):
    """Load the Keras model. Cached to avoid reloading."""
    path = model_path or MODEL_PATH
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"model.keras not found at: {path}")
        return tf.keras.models.load_model(path)
    except Exception as e:
        logger.error(f"Failed to load model from {path}: {e}")
        try:
            st.error(
                f"Error loading model. Please ensure '{os.path.basename(path)}' exists and is valid. Details: {e}"
            )
        except Exception:
            pass
        return None


def check_mri_quality(img_array: np.ndarray) -> tuple[bool, str]:
    """
    Check if the image looks like an MRI.
    MRIs are generally grayscale and have some variance.
    Returns (is_valid, reason)
    """
    # Check size
    if img_array.shape[0] < 50 or img_array.shape[1] < 50:
        return False, "Image is too small (under 50x50)."

    # Check standard deviation (uniform image)
    std_dev = np.std(img_array)
    if std_dev < 10:
        return False, "Image is too uniform. Does not look like an MRI."

    # Check color variance (MRIs are grayscale so R, G, B should be similar)
    if img_array.ndim == 3 and img_array.shape[-1] == 3:
        r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
        color_diff = (
            np.mean(np.abs(r - g))
            + np.mean(np.abs(g - b))
            + np.mean(np.abs(r - b))
        )
        # If it's very colorful, color_diff will be high.
        if color_diff > 45:
            return False, "Image has too much color variance. Please upload a grayscale MRI scan."

    return True, ""


def strip_exif(img: Image.Image) -> Image.Image:
    """Strip EXIF metadata from the image to protect user privacy."""
    return Image.frombytes(img.mode, img.size, img.tobytes())


def validate_image(img: Image.Image) -> Image.Image:
    """Validate and convert image to RGB. Handles RGBA and Grayscale. Strips EXIF."""
    if img is None:
        raise ValueError("No image provided.")
    try:
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Check quality
        img_array = np.array(img)
        is_valid, reason = check_mri_quality(img_array)
        if not is_valid:
            raise ValueError(f"Image Quality Check Failed: {reason}")

        return strip_exif(img)
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Image conversion failed: {e}")
        raise ValueError("Failed to process the image format.") from e


def preprocess_image(img: Image.Image) -> np.ndarray:
    """Resize and preprocess image for the model."""
    try:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img_resized = img.resize(INPUT_SHAPE)
        # Keep float32 0-255 as per constraints (model rescales internally)
        img_array = np.array(img_resized, dtype="float32")
        img_expanded = np.expand_dims(img_array, axis=0)
        return img_expanded
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise ValueError(
            "Failed to preprocess the uploaded image. Please ensure it is a valid image file."
        ) from e


def predict(model, img_array: np.ndarray) -> np.ndarray:
    """Run model prediction."""
    try:
        pred = model.predict(img_array, verbose=0)
        return pred[0]
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise RuntimeError("Failed to analyze the image.") from e


def get_gradcam_heatmap(model, img_array: np.ndarray) -> np.ndarray:
    """
    Generate Grad-CAM heatmap for a model containing a MobileNetV2 backbone.
    If it fails, returns None.
    """
    try:
        # Find base model layer (either by name containing mobilenet or by type tf.keras.Model)
        base_model = None
        base_idx = -1
        for idx, layer in enumerate(model.layers):
            if "mobilenet" in layer.name.lower() or isinstance(layer, tf.keras.Model) or hasattr(layer, "layers"):
                base_model = layer
                base_idx = idx
                break

        if base_model is None:
            logger.warning("No backbone model layer found for Grad-CAM.")
            return None

        # Find the last convolutional / activation layer in base_model
        last_conv_layer_name = "out_relu"
        try:
            last_conv_layer = base_model.get_layer(last_conv_layer_name)
        except ValueError:
            conv_layers = [
                l for l in base_model.layers
                if "conv" in l.name.lower() or "relu" in l.name.lower() or "out" in l.name.lower()
            ]
            if not conv_layers:
                return None
            last_conv_layer = conv_layers[-1]

        last_conv_layer_model = tf.keras.Model(base_model.inputs, last_conv_layer.output)

        classifier_input = tf.keras.Input(shape=last_conv_layer.output.shape[1:])
        x = classifier_input
        for layer in model.layers[base_idx + 1:]:
            x = layer(x)
        classifier_model = tf.keras.Model(classifier_input, x)

        # Forward pass through layers before base_model (e.g. Rescaling)
        pre_input = tf.cast(img_array, tf.float32)
        for layer in model.layers[:base_idx]:
            if not isinstance(layer, tf.keras.layers.InputLayer):
                pre_input = layer(pre_input)

        with tf.GradientTape() as tape:
            last_conv_layer_output = last_conv_layer_model(pre_input)
            tape.watch(last_conv_layer_output)
            preds = classifier_model(last_conv_layer_output)
            top_pred_index = tf.argmax(preds[0])
            top_class_channel = preds[:, top_pred_index]

        grads = tape.gradient(top_class_channel, last_conv_layer_output)
        if grads is None:
            return None
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        last_conv_layer_output = last_conv_layer_output[0]
        heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0)
        max_val = tf.math.reduce_max(heatmap)
        # Guard against divide-by-zero when all activations are non-positive
        if max_val == 0:
            return None
        heatmap = heatmap / max_val
        return heatmap.numpy()
    except Exception as e:
        logger.error(f"Grad-CAM failed: {e}")
        return None


def overlay_gradcam(img: Image.Image, heatmap: np.ndarray, alpha: float = 0.4) -> Image.Image:
    """Overlay Grad-CAM heatmap on the original image."""
    if heatmap is None:
        return img

    img_resized = img.resize(INPUT_SHAPE)
    img_array = np.array(img_resized.convert("RGB"), dtype=np.float32)

    # Ensure heatmap is 2D float32
    heatmap_2d = np.squeeze(heatmap).astype(np.float32)
    heatmap_uint8 = np.uint8(255 * np.clip(heatmap_2d, 0.0, 1.0))

    # Resize heatmap to match INPUT_SHAPE using PIL (pure Python/NumPy, no cv2 required)
    heatmap_img = Image.fromarray(heatmap_uint8, mode="L").resize(INPUT_SHAPE, Image.Resampling.BILINEAR)
    heatmap_resized = np.array(heatmap_img)

    # Apply Jet colormap via pure NumPy LUT
    jet = _JET_LUT[heatmap_resized].astype(np.float32)

    superimposed_img = jet * alpha + img_array * (1.0 - alpha)
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)

    return Image.fromarray(superimposed_img).resize(img.size, Image.Resampling.LANCZOS)
