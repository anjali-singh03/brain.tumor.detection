# Brain Tumor Detection App 🧠

**🔗 Live demo:**(https://braintumordetection-b5wdbnx5ym5mybrbvomyvd.streamlit.app/)

A Streamlit web app that classifies brain MRI scans into four classes using a CNN (MobileNetV2 transfer learning).

> ⚠️ For educational purposes only. Not a diagnostic tool.

## Features
- Upload an MRI image (JPG/PNG)
- Get a predicted class with confidence: glioma, meningioma, pituitary, or no tumor
- Runs fully in the browser with a locally loaded model

## Model
- **Dataset:** [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset) (7,200 images, 4 classes)
- **Architecture:** MobileNetV2 (ImageNet weights, frozen) + GlobalAveragePooling + Dropout + Dense (softmax)
- **Input size:** 160 x 160
- **Training:** 3 epochs, Adam optimizer
- **Validation accuracy:** ~84.8%

## Tech Stack
Python, TensorFlow/Keras, Streamlit, Pillow, NumPy

## Run Locally
```bash
pip install -r requirements.txt
streamlit run braintumorapp.py
```

## Project Structure
```
├── braintumorapp.py    # Streamlit app
├── model.keras         # Trained model
├── model train         # Training code
├── requirements.txt
└── screenshot.png
```

## Screenshot
![App Screenshot](screenshot.png)

## Author
Anjali Singh
