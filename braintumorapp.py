import streamlit as st
from google.cloud import aiplatform
from utils.preprocess import preprocess_image

# Vertex AI config
PROJECT_ID = "aqueous-heading-463906-b9"
REGION = "us-central1"
ENDPOINT_ID = "YOUR_NEW_ENDPOINT_ID"  # Replace with correct endpoint

aiplatform.init(project=PROJECT_ID, location=REGION)
endpoint = aiplatform.Endpoint(ENDPOINT_ID)

st.title("🧠 Brain Tumor Detection App")
st.write("Upload an MRI image to check for brain tumor.")

uploaded_file = st.file_uploader("Upload MRI image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    img_array = preprocess_image(uploaded_file)

    prediction = endpoint.predict(instances=img_array)
    pred_value = prediction.predictions[0][0]

    if pred_value > 0.5:
        st.error("🧠 Tumor Detected")
    else:
        st.success("✅ No Tumor Detected")
