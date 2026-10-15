# config.py
# Constants and configuration for the Brain Tumor Detection App
import os

# Class labels in the exact order required by the model
CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]

# UI Colors for each class
COLORS = {
    "glioma": "#e74c3c",
    "meningioma": "#e67e22",
    "pituitary": "#f1c40f",
    "notumor": "#2ecc71"
}

# Root directory of the project (one level above this config file's directory)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Sample image paths — anchored to project root so they work regardless of CWD
SAMPLES = {c: os.path.join(_PROJECT_ROOT, f"{c}.jpg") for c in CLASSES}

# Model input configuration
INPUT_SHAPE = (160, 160)

# Default model path
MODEL_PATH = os.path.join(_PROJECT_ROOT, "model.keras")

