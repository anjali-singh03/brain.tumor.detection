"""
conftest.py
Shared fixtures for the Brain Tumor Detection test suite.
"""
import numpy as np
import pytest
from PIL import Image


@pytest.fixture
def rgb_mri_image():
    """A grayscale-like RGB MRI image (equal R/G/B channels) with sufficient variance.

    Uses equal channel values so the color-variance heuristic in check_mri_quality
    does not reject it (color_diff ≈ 0 which is well below the 45 threshold).
    """
    rng = np.random.default_rng(42)
    gray = rng.integers(30, 220, (200, 200), dtype=np.uint8)
    arr = np.stack([gray, gray, gray], axis=-1)  # R == G == B
    return Image.fromarray(arr, "RGB")


@pytest.fixture
def grayscale_mri_image():
    """A realistic pseudo-MRI grayscale (L-mode) image."""
    rng = np.random.default_rng(42)
    arr = rng.integers(30, 220, (200, 200), dtype=np.uint8)
    return Image.fromarray(arr, "L")


@pytest.fixture
def rgba_mri_image():
    """A grayscale-like RGBA MRI image (equal R/G/B, full alpha).

    After RGBA→RGB conversion the color-variance check must pass.
    """
    rng = np.random.default_rng(42)
    gray = rng.integers(30, 220, (200, 200), dtype=np.uint8)
    alpha = np.full((200, 200), 255, dtype=np.uint8)
    arr = np.stack([gray, gray, gray, alpha], axis=-1)
    return Image.fromarray(arr, "RGBA")


@pytest.fixture
def uniform_image():
    """A completely uniform (solid colour) image — fails MRI quality check."""
    arr = np.full((200, 200, 3), 128, dtype=np.uint8)
    return Image.fromarray(arr, "RGB")


@pytest.fixture
def tiny_image():
    """An image smaller than the 50×50 minimum threshold."""
    rng = np.random.default_rng(42)
    arr = rng.integers(0, 255, (40, 40, 3), dtype=np.uint8)
    return Image.fromarray(arr, "RGB")


@pytest.fixture
def colorful_image():
    """A highly colorful (non-grayscale) image — fails MRI color check."""
    arr = np.zeros((200, 200, 3), dtype=np.uint8)
    arr[:, :, 0] = 200   # Strong red channel
    arr[:, :, 1] = 20    # Very low green
    arr[:, :, 2] = 180   # Strong blue
    return Image.fromarray(arr, "RGB")
