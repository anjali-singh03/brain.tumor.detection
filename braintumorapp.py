import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image

st.title("Brain Tumor Detection App 🧠")
st.caption("For educational purposes only, not a diagnostic tool.")

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model.keras")

model = load_model()
classes = ["glioma", "meningioma", "notumor", "pituitary"]

file = st.file_uploader("Upload MRI image", type=["jpg", "jpeg", "png"])
if file:
    img = Image.open(file).convert("RGB")
    st.image(img, width=300)
    x = np.expand_dims(np.array(img.resize((160, 160)), dtype="float32"), 0)
    pred = model.predict(x)[0]
    st.success(f"Prediction: {classes[int(np.argmax(pred))]} ({pred.max()*100:.1f}%)")
