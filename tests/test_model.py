import pytest
import numpy as np
import os
from PIL import Image
from src.inference import load_model, predict, preprocess_image
from src.config import CLASSES, SAMPLES, INPUT_SHAPE


def test_prediction_output_sums_to_1():
    try:
        model = load_model()
    except Exception:
        pytest.skip("Model not available for testing")

    if model is None:
        pytest.skip("Model not available for testing")

    # Dummy input
    dummy_input = np.random.rand(1, INPUT_SHAPE[0], INPUT_SHAPE[1], 3).astype(np.float32) * 255.0
    pred = predict(model, dummy_input)

    # Assert length is 4 (number of classes)
    assert len(pred) == len(CLASSES), f"Prediction should have {len(CLASSES)} probabilities"

    # Assert all values are valid probabilities [0, 1]
    assert np.all(pred >= 0.0) and np.all(pred <= 1.0), "Probabilities must be in range [0, 1]"

    # Assert sum is close to 1
    assert np.isclose(np.sum(pred), 1.0, atol=1e-5), "Prediction probabilities must sum to 1"


@pytest.mark.parametrize("class_name", CLASSES)
def test_sample_image_prediction(class_name):
    """Test prediction on each bundled sample image."""
    try:
        model = load_model()
    except Exception:
        pytest.skip("Model not available for testing")

    if model is None:
        pytest.skip("Model not available for testing")

    sample_path = SAMPLES.get(class_name)
    if not sample_path or not os.path.exists(sample_path):
        pytest.skip(f"Sample image for {class_name} not found")

    img = Image.open(sample_path)
    x = preprocess_image(img)
    pred = predict(model, x)

    assert len(pred) == len(CLASSES)
    assert np.isclose(np.sum(pred), 1.0, atol=1e-5)
