"""
test_inference.py
Tests for image preprocessing, validation, MRI quality checks, and Grad-CAM explainability.
"""
import numpy as np
import pytest
from PIL import Image

from src.inference import (
    preprocess_image, validate_image, check_mri_quality, strip_exif,
    get_gradcam_heatmap, overlay_gradcam, load_model
)
from src.config import INPUT_SHAPE


# ---------------------------------------------------------------------------
# validate_image — mode conversion
# ---------------------------------------------------------------------------

class TestValidateImageConversion:
    """validate_image must convert any mode to RGB and strip EXIF."""

    def test_rgba_converts_to_rgb(self, rgba_mri_image):
        result = validate_image(rgba_mri_image)
        assert result.mode == "RGB"

    def test_grayscale_converts_to_rgb(self, grayscale_mri_image):
        result = validate_image(grayscale_mri_image)
        assert result.mode == "RGB"

    def test_rgb_passes_through(self, rgb_mri_image):
        result = validate_image(rgb_mri_image)
        assert result.mode == "RGB"

    def test_none_raises_value_error(self):
        with pytest.raises(ValueError, match="No image provided"):
            validate_image(None)


# ---------------------------------------------------------------------------
# validate_image — MRI quality gate
# ---------------------------------------------------------------------------

class TestValidateImageQuality:
    """validate_image must reject images that fail MRI quality heuristics."""

    def test_uniform_image_rejected(self, uniform_image):
        with pytest.raises(ValueError, match="Image Quality Check Failed"):
            validate_image(uniform_image)

    def test_tiny_image_rejected(self, tiny_image):
        with pytest.raises(ValueError, match="Image Quality Check Failed"):
            validate_image(tiny_image)

    def test_colorful_image_rejected(self, colorful_image):
        with pytest.raises(ValueError, match="Image Quality Check Failed"):
            validate_image(colorful_image)


# ---------------------------------------------------------------------------
# check_mri_quality
# ---------------------------------------------------------------------------

class TestCheckMriQuality:

    def test_valid_mri_passes(self, rgb_mri_image):
        arr = np.array(rgb_mri_image)
        valid, reason = check_mri_quality(arr)
        assert valid is True
        assert reason == ""

    def test_too_small_fails(self):
        arr = np.zeros((40, 40, 3), dtype=np.uint8)
        valid, reason = check_mri_quality(arr)
        assert valid is False
        assert "too small" in reason.lower()

    def test_uniform_image_fails(self):
        arr = np.full((200, 200, 3), 128, dtype=np.uint8)
        valid, reason = check_mri_quality(arr)
        assert valid is False
        assert "uniform" in reason.lower()

    def test_colorful_image_fails(self):
        arr = np.zeros((200, 200, 3), dtype=np.uint8)
        arr[:, :, 0] = 200
        arr[:, :, 1] = 10
        arr[:, :, 2] = 190
        valid, reason = check_mri_quality(arr)
        assert valid is False
        assert "color" in reason.lower()

    def test_grayscale_array_passes(self):
        """Grayscale arrays (2-D) should not trigger the color variance check."""
        rng = np.random.default_rng(0)
        arr = rng.integers(30, 220, (200, 200), dtype=np.uint8)
        valid, reason = check_mri_quality(arr)
        assert valid is True


# ---------------------------------------------------------------------------
# strip_exif
# ---------------------------------------------------------------------------

class TestStripExif:

    def test_output_mode_preserved(self, rgb_mri_image):
        stripped = strip_exif(rgb_mri_image)
        assert stripped.mode == rgb_mri_image.mode

    def test_output_size_preserved(self, rgb_mri_image):
        stripped = strip_exif(rgb_mri_image)
        assert stripped.size == rgb_mri_image.size

    def test_pixel_data_unchanged(self, rgb_mri_image):
        stripped = strip_exif(rgb_mri_image)
        orig = np.array(rgb_mri_image)
        result = np.array(stripped)
        np.testing.assert_array_equal(orig, result)


# ---------------------------------------------------------------------------
# preprocess_image
# ---------------------------------------------------------------------------

class TestPreprocessImage:

    def test_output_shape(self, rgb_mri_image):
        processed = preprocess_image(rgb_mri_image)
        assert processed.shape == (1, INPUT_SHAPE[0], INPUT_SHAPE[1], 3)

    def test_output_dtype(self, rgb_mri_image):
        processed = preprocess_image(rgb_mri_image)
        assert processed.dtype == np.float32

    def test_pixel_value_range(self, rgb_mri_image):
        processed = preprocess_image(rgb_mri_image)
        assert np.min(processed) >= 0.0
        assert np.max(processed) <= 255.0

    def test_non_square_input_resizes_correctly(self):
        """Non-square images must be resized to the exact INPUT_SHAPE."""
        img = Image.new("RGB", (300, 500), (128, 64, 32))
        processed = preprocess_image(img)
        assert processed.shape == (1, INPUT_SHAPE[0], INPUT_SHAPE[1], 3)

    def test_grayscale_input_converted_to_3_channels(self, grayscale_mri_image):
        """Grayscale input must produce 3 channels."""
        processed = preprocess_image(grayscale_mri_image)
        assert processed.shape == (1, INPUT_SHAPE[0], INPUT_SHAPE[1], 3)

    def test_white_image_max_value(self):
        """All-white image should produce max pixel value of 255."""
        img = Image.new("RGB", (200, 200), (255, 255, 255))
        processed = preprocess_image(img)
        assert np.max(processed) == pytest.approx(255.0)

    def test_black_image_min_value(self):
        """All-black image should produce min pixel value of 0."""
        img = Image.new("RGB", (200, 200), (0, 0, 0))
        processed = preprocess_image(img)
        assert np.min(processed) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Grad-CAM and Overlay Tests
# ---------------------------------------------------------------------------

class TestGradCamAndOverlay:

    def test_overlay_gradcam_none_heatmap_returns_original(self, rgb_mri_image):
        result = overlay_gradcam(rgb_mri_image, None)
        assert result.size == rgb_mri_image.size

    def test_overlay_gradcam_with_2d_heatmap(self, rgb_mri_image):
        # 5x5 heatmap (MobileNetV2 last conv layer output size)
        heatmap = np.random.rand(5, 5).astype(np.float32)
        result = overlay_gradcam(rgb_mri_image, heatmap)
        assert isinstance(result, Image.Image)
        assert result.size == rgb_mri_image.size
        assert result.mode == "RGB"

    def test_overlay_gradcam_with_varying_input_sizes(self):
        img = Image.new("RGB", (400, 600), (100, 100, 100))
        heatmap = np.random.rand(5, 5).astype(np.float32)
        result = overlay_gradcam(img, heatmap)
        assert result.size == (400, 600)
        assert result.mode == "RGB"

    def test_gradcam_heatmap_generation_with_model(self, rgb_mri_image):
        try:
            model = load_model()
        except Exception:
            pytest.skip("Model not available for Grad-CAM test")

        if model is None:
            pytest.skip("Model not available for Grad-CAM test")

        x = preprocess_image(rgb_mri_image)
        heatmap = get_gradcam_heatmap(model, x)
        assert heatmap is not None
        assert isinstance(heatmap, np.ndarray)
        assert heatmap.ndim == 2
        assert np.min(heatmap) >= 0.0
        assert np.max(heatmap) <= 1.0 + 1e-5
