import os
import streamlit as st
import numpy as np
import tensorflow as tf
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(page_title="Brain Tumor Detection", page_icon="🧠", layout="wide")

CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]
COLORS = {"glioma": "#e74c3c", "meningioma": "#e67e22", "pituitary": "#f1c40f", "notumor": "#2ecc71"}
SAMPLES = {c: f"{c}.jpg" for c in CLASSES}

st.markdown(
    """
<style>
.hero {padding: 22px 26px; border-radius: 16px; color: white; margin-bottom: 18px;
       background: linear-gradient(120deg,#6a11cb,#2575fc 60%,#00c6ff);}
.hero h1 {margin: 0; font-size: 2.1rem;}
.hero p {margin: 6px 0 0; opacity: .95;}
.card {padding: 18px 20px; border-radius: 14px; color: white; margin-bottom: 10px;}
.card h2 {margin: 0;}
.card p {margin: 6px 0 0; opacity: .95;}
</style>
""",
    unsafe_allow_html=True,
)

DATA = {
    "glioma": {
        "title": "Glioma", "emoji": "🔴",
        "overview": "A tumor that starts in glial cells, the supporting cells of the brain and spinal cord. Gliomas range from slow-growing (low grade) to aggressive (high grade) and are among the most common primary brain tumors.",
        "causes": [
            "Exact cause is usually unknown",
            "Past exposure to ionizing radiation (for example radiotherapy to the head)",
            "Rare inherited syndromes: neurofibromatosis, Li-Fraumeni syndrome, tuberous sclerosis",
            "Risk rises with age; no proven link to mobile phones",
        ],
        "symptoms": [
            "Headaches that keep getting worse, often worse in the morning",
            "Seizures", "Nausea or vomiting",
            "Memory, speech or personality changes",
            "Weakness, numbness or balance problems on one side",
        ],
        "treatment": [
            "Surgery to remove as much of the tumor as safely possible",
            "Radiotherapy to destroy remaining tumor cells",
            "Chemotherapy (for example temozolomide in some types)",
            "Medicines for symptom control: anti-seizure drugs, steroids for swelling",
            "Regular follow-up MRI scans; treatment depends on grade, location and patient health",
        ],
        "precautions": [
            "Take anti-seizure medicines exactly as prescribed",
            "Do not miss follow-up MRI scans and appointments",
            "Avoid unnecessary radiation exposure (only medically needed CT/X-ray)",
            "Avoid driving if you have had seizures, until your doctor allows it",
            "Eat balanced meals, sleep well, and ask about safe physical activity",
            "Seek emotional support: counselling and support groups help",
        ],
        "specialists": "Neurologist, neurosurgeon, neuro-oncologist, radiation oncologist",
        "see_doctor": [
            "New or worsening headaches that do not settle",
            "Any seizure, even a single one",
            "Sudden vision, speech or balance problems",
        ],
        "questions": [
            "What grade and type is this tumor?",
            "Is surgery possible, and what are the risks?",
            "What treatment options do I have and what are their side effects?",
            "How often will I need follow-up scans?",
        ],
    },
    "meningioma": {
        "title": "Meningioma", "emoji": "🟠",
        "overview": "A tumor that grows from the meninges, the protective layers covering the brain and spinal cord. Most meningiomas are benign (non-cancerous) and grow slowly, so some are only monitored.",
        "causes": [
            "Exact cause is mostly unknown",
            "Previous radiation to the head",
            "Being female and older age (hormonal influence is suspected)",
            "Inherited condition neurofibromatosis type 2 (NF2)",
        ],
        "symptoms": [
            "Slowly worsening headaches",
            "Blurred or double vision",
            "Hearing loss or ringing in the ears",
            "Seizures", "Memory problems or weakness in arms or legs",
        ],
        "treatment": [
            "Watchful waiting with regular MRI for small, symptom-free tumors",
            "Surgery to remove the tumor (often curative for accessible ones)",
            "Radiotherapy or stereotactic radiosurgery when surgery is risky or tumor remains",
            "Medicines for seizures or swelling if needed",
        ],
        "precautions": [
            "Keep all scheduled monitoring scans",
            "Report new symptoms early, especially vision or hearing changes",
            "Avoid unnecessary head radiation",
            "Discuss hormone therapy with your doctor if you use it",
            "Maintain a healthy weight, diet and sleep routine",
        ],
        "specialists": "Neurologist, neurosurgeon, radiation oncologist, ophthalmologist (if vision is affected)",
        "see_doctor": [
            "Gradual vision loss or double vision",
            "Persistent headaches or hearing changes",
            "Any seizure",
        ],
        "questions": [
            "Can this be safely monitored instead of treated now?",
            "How fast is it growing?",
            "What are the surgery and radiation options?",
            "What symptoms should make me call you urgently?",
        ],
    },
    "pituitary": {
        "title": "Pituitary Tumor", "emoji": "🟡",
        "overview": "A growth in the pituitary gland at the base of the brain, which controls hormones. Most are benign adenomas. They can press on nearby nerves or produce too much (or too little) hormone.",
        "causes": [
            "Usually no clear cause",
            "A few are linked to inherited conditions such as MEN1",
            "Hormone-related gene changes inside the gland's cells",
        ],
        "symptoms": [
            "Headaches",
            "Vision problems, especially loss of side vision",
            "Hormone effects: fatigue, weight change, irregular periods, milk discharge, low sex drive",
            "Growth changes (in some hormone-producing types)",
        ],
        "treatment": [
            "Medicines that shrink some tumors or block hormone excess (for example for prolactinomas)",
            "Transsphenoidal surgery (through the nose) to remove the tumor",
            "Radiotherapy if tumor remains or returns",
            "Hormone replacement if the gland is under-active after treatment",
        ],
        "precautions": [
            "Get regular hormone blood tests as advised",
            "Take hormone medicines on time and never stop suddenly",
            "Get eyesight checked regularly",
            "Report new vision changes or severe sudden headache immediately",
            "Keep follow-up MRI appointments",
        ],
        "specialists": "Endocrinologist, neurosurgeon, ophthalmologist",
        "see_doctor": [
            "Vision loss or narrowing of your side vision",
            "Sudden severe headache with vision change or vomiting",
            "Unexplained hormone symptoms (periods, fatigue, weight)",
        ],
        "questions": [
            "Is the tumor producing hormones?",
            "Can medicine alone treat it?",
            "Will I need lifelong hormone tablets?",
            "How will my vision be monitored?",
        ],
    },
    "notumor": {
        "title": "No Tumor Detected", "emoji": "🟢",
        "overview": "The model did not find a tumor pattern in this scan. This is only an automated estimate, and it cannot rule out other brain conditions or small abnormalities.",
        "causes": ["Not applicable: no tumor pattern was detected"],
        "symptoms": ["A normal-looking result does not explain existing symptoms. Persisting symptoms still need medical review."],
        "treatment": ["No tumor treatment is suggested by this result", "Symptoms should be assessed by a doctor"],
        "precautions": [
            "Keep a healthy routine: sleep, hydration, exercise, stress management",
            "Protect your head during sports and driving",
            "Do not ignore ongoing headaches, dizziness or vision changes",
        ],
        "specialists": "General physician or neurologist if symptoms continue",
        "see_doctor": [
            "Headaches that keep returning or worsen",
            "Seizures, fainting or sudden weakness",
            "Vision, speech or balance problems",
        ],
        "questions": [
            "Could my symptoms have another cause?",
            "Do I need a radiologist to review this scan?",
        ],
    },
}

CASES = {
    "glioma": {
        "patient": "Illustrative case: a 42-year-old office worker",
        "happened": "Had weeks of morning headaches, then a first seizure at work. An MRI showed a mass in the temporal lobe, and a biopsy confirmed a low-grade glioma.",
        "doctors": "The team explained that surgery would remove as much of the tumor as safely possible, followed by radiotherapy if needed. They started anti-seizure medicine, advised no driving for a period, and planned MRI scans every few months.",
        "outcome": "Returned to work after recovery and continues regular scans. Outcomes depend on tumor grade and location.",
        "links": [
            ("PubMed: glioma case reports", "https://pubmed.ncbi.nlm.nih.gov/?term=glioma+case+report"),
            ("NHS: Brain tumours", "https://www.nhs.uk/conditions/brain-tumours/"),
            ("American Brain Tumor Association", "https://www.abta.org"),
        ],
    },
    "meningioma": {
        "patient": "Illustrative case: a 58-year-old woman",
        "happened": "Noticed slowly blurring vision and mild headaches. An MRI found a small meningioma pressing near the optic nerve.",
        "doctors": "Doctors explained that most meningiomas are benign and slow growing. They started with regular MRI monitoring, and recommended surgery or radiosurgery once the tumor grew and vision was affected.",
        "outcome": "Treatment stopped further vision loss. She continues yearly follow-up scans.",
        "links": [
            ("PubMed: meningioma case reports", "https://pubmed.ncbi.nlm.nih.gov/?term=meningioma+case+report"),
            ("NHS: Brain tumours", "https://www.nhs.uk/conditions/brain-tumours/"),
            ("American Brain Tumor Association", "https://www.abta.org"),
        ],
    },
    "pituitary": {
        "patient": "Illustrative case: a 30-year-old woman",
        "happened": "Had irregular periods, unexpected milk discharge and headaches. Blood tests showed very high prolactin, and an MRI found a small pituitary adenoma.",
        "doctors": "The endocrinologist explained that this type (a prolactinoma) is often treated with tablets rather than surgery, with blood tests and an eye check to monitor progress.",
        "outcome": "Hormone levels returned to normal on medication and the tumor shrank. Surgery is kept as a backup option.",
        "links": [
            ("PubMed: pituitary adenoma case reports", "https://pubmed.ncbi.nlm.nih.gov/?term=pituitary+adenoma+case+report"),
            ("NHS: Brain tumours", "https://www.nhs.uk/conditions/brain-tumours/"),
            ("American Brain Tumor Association", "https://www.abta.org"),
        ],
    },
    "notumor": {
        "patient": "Illustrative case: a 27-year-old student",
        "happened": "Had recurring headaches and worried about a tumor. An MRI showed no tumor or other serious abnormality.",
        "doctors": "The doctor explained that stress, poor sleep, long screen time and migraine are common causes. They advised regular sleep, hydration, a headache diary and a review if symptoms change.",
        "outcome": "Headaches improved with lifestyle changes. The doctor asked her to return if new symptoms appeared.",
        "links": [
            ("NHS: Headaches", "https://www.nhs.uk/conditions/headaches/"),
        ],
    },
}


@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model.keras")


# ---------------- helpers ----------------
def box(kind, items):
    text = "\n".join(f"- {i}" for i in items)
    {"info": st.info, "warning": st.warning, "success": st.success, "error": st.error}[kind](text)


def card(title, sub, color):
    st.markdown(
        f'<div class="card" style="background:linear-gradient(135deg,{color},#111827)">'
        f"<h2>{title}</h2><p>{sub}</p></div>",
        unsafe_allow_html=True,
    )


def style(fig, height=300):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def gauge(conf, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=conf, number={"suffix": "%"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": color},
               "steps": [{"range": [0, 50], "color": "#fadbd8"},
                         {"range": [50, 70], "color": "#fdebd0"},
                         {"range": [70, 100], "color": "#d5f5e3"}]}))
    return style(fig, 250)


def donut(pred):
    fig = go.Figure(go.Pie(
        labels=[DATA[c]["title"] for c in CLASSES], values=[float(p) for p in pred],
        hole=0.55, sort=False, marker=dict(colors=[COLORS[c] for c in CLASSES])))
    return style(fig)


def bars(pred):
    fig = go.Figure(go.Bar(
        x=[float(p) * 100 for p in pred], y=[DATA[c]["title"] for c in CLASSES], orientation="h",
        marker_color=[COLORS[c] for c in CLASSES],
        text=[f"{p * 100:.1f}%" for p in pred], textposition="auto"))
    fig.update_layout(xaxis_title="Probability (%)")
    return style(fig)


def show_tabs(key):
    d = DATA[key]
    tabs = st.tabs(["📖 Overview", "🧬 Causes", "🩺 Symptoms", "💊 Treatment",
                    "🛡️ Precautions", "👨‍⚕️ Doctor's Advice", "📝 Patient Stories"])
    with tabs[0]:
        st.info(d["overview"])
    with tabs[1]:
        box("warning", d["causes"])
    with tabs[2]:
        box("error", d["symptoms"])
    with tabs[3]:
        box("success", d["treatment"])
        st.caption("Treatment always depends on the doctor's assessment.")
    with tabs[4]:
        box("info", d["precautions"])
    with tabs[5]:
        st.success(f"**Which specialist to see:** {d['specialists']}")
        st.markdown("**See a doctor if you notice:**")
        box("warning", d["see_doctor"])
        st.markdown("**Questions to ask your doctor:**")
        box("info", d["questions"])
        st.error("Emergency: sudden severe headache, seizure, loss of vision, weakness or confusion needs immediate medical care.")
    with tabs[6]:
        c = CASES[key]
        st.caption("Illustrative example written for education. Not a real patient. Real experiences vary.")
        st.markdown(f"**Patient:** {c['patient']}")
        st.info(f"**What happened:** {c['happened']}")
        st.success(f"**What the doctors explained:** {c['doctors']}")
        st.markdown(f"**Outcome:** {c['outcome']}")
        st.divider()
        st.markdown("**Read real published case reports and guides:**")
        for name, url in c["links"]:
            st.markdown(f"- [{name}]({url})")


def get_image():
    source = st.radio("Image source", ["📤 Upload my own", "🖼️ Try a sample"], horizontal=True)
    if source.startswith("📤"):
        f = st.file_uploader("Upload MRI image", type=["jpg", "jpeg", "png"])
        return (Image.open(f).convert("RGB"), None) if f else (None, None)
    available = [c for c in CLASSES if os.path.exists(SAMPLES[c])]
    if not available:
        st.info("No sample images found in the repo yet.")
        return None, None
    true = st.selectbox("Pick a sample scan", available, format_func=lambda k: f"{DATA[k]['emoji']} {DATA[k]['title']} sample")
    return Image.open(SAMPLES[true]).convert("RGB"), true


# ---------------- pages ----------------
def analyze_page():
    img, true = get_image()
    if img is None:
        st.info("👆 Upload an MRI image or try a sample to begin.")
        return

    model = load_model()
    x = np.expand_dims(np.array(img.resize((160, 160)), dtype="float32"), 0)
    with st.spinner("Analyzing scan..."):
        pred = model.predict(x, verbose=0)[0]
    idx = int(np.argmax(pred))
    label = CLASSES[idx]
    conf = float(pred[idx]) * 100

    col1, col2 = st.columns([1, 1.3])
    with col1:
        st.image(img, caption="MRI scan", width=380)
    with col2:
        card(f"{DATA[label]['emoji']} {DATA[label]['title']}", f"Model confidence: {conf:.1f}%", COLORS[label])
        st.plotly_chart(gauge(conf, COLORS[label]), key="gauge")

    if conf < 70:
        st.warning("Low confidence. Treat this result with extra caution.")
    if true:
        if true == label:
            st.success(f"✅ Prediction matches the true label of this sample ({DATA[true]['title']}).")
        else:
            st.error(f"❌ The true label of this sample is {DATA[true]['title']}, but the model predicted {DATA[label]['title']}. This shows the model is not perfect.")

    st.subheader("📈 Prediction breakdown")
    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(donut(pred), key="donut")
    with g2:
        st.plotly_chart(bars(pred), key="bars")

    st.divider()
    st.subheader("About this condition")
    show_tabs(label)

    report = (
        "BRAIN TUMOR DETECTION REPORT (educational use only)\n"
        f"Prediction: {DATA[label]['title']}\nConfidence: {conf:.1f}%\n\n"
        f"Overview: {DATA[label]['overview']}\n\n"
        f"Specialist: {DATA[label]['specialists']}\n\n"
        "This is not a medical diagnosis. Consult a qualified doctor."
    )
    st.download_button("⬇️ Download report", report, file_name="report.txt")


def learn_page():
    choice = st.selectbox("Select a condition", CLASSES,
                          format_func=lambda k: f"{DATA[k]['emoji']} {DATA[k]['title']}")
    col1, col2 = st.columns([1, 2])
    with col1:
        if os.path.exists(SAMPLES[choice]):
            st.image(Image.open(SAMPLES[choice]), caption=f"Sample MRI: {DATA[choice]['title']}", width=300)
        else:
            st.info("Sample image not added yet.")
    with col2:
        card(f"{DATA[choice]['emoji']} {DATA[choice]['title']}", DATA[choice]["overview"], COLORS[choice])
        st.markdown(f"**Specialist:** {DATA[choice]['specialists']}")
    show_tabs(choice)


def performance_page():
    st.subheader("📊 Model performance")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Validation accuracy", "84.8%")
    m2.metric("Training accuracy", "89.1%")
    m3.metric("Epochs", "3")
    m4.metric("Input size", "160 x 160")

    epochs = [1, 2, 3]
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=epochs, y=[75.7, 87.1, 89.1], mode="lines+markers", name="Training", line=dict(color="#2ecc71", width=3)))
        fig.add_trace(go.Scatter(x=epochs, y=[83.1, 83.4, 84.8], mode="lines+markers", name="Validation", line=dict(color="#3498db", width=3)))
        fig.update_layout(title="Accuracy per epoch (%)", xaxis_title="Epoch", xaxis=dict(dtick=1))
        st.plotly_chart(style(fig, 320), key="acc")
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=epochs, y=[0.5972, 0.3522, 0.2916], mode="lines+markers", name="Training", line=dict(color="#e67e22", width=3)))
        fig.add_trace(go.Scatter(x=epochs, y=[0.5445, 0.5762, 0.5527], mode="lines+markers", name="Validation", line=dict(color="#e74c3c", width=3)))
        fig.update_layout(title="Loss per epoch", xaxis_title="Epoch", xaxis=dict(dtick=1))
        st.plotly_chart(style(fig, 320), key="loss")

    c3, c4 = st.columns(2)
    with c3:
        fig = go.Figure(go.Pie(labels=["Training images", "Testing images"], values=[5600, 1600], hole=0.55,
                               marker=dict(colors=["#8e44ad", "#1abc9c"])))
        fig.update_layout(title="Dataset split (7,200 images)")
        st.plotly_chart(style(fig, 320), key="split")
    with c4:
        st.markdown("**Model details**")
        st.markdown(
            "- Architecture: MobileNetV2 (ImageNet weights, frozen) + pooling + dropout + dense softmax\n"
            "- Classes: glioma, meningioma, pituitary, no tumor\n"
            "- Optimizer: Adam, loss: sparse categorical cross-entropy\n"
            "- Dataset: Brain Tumor MRI Dataset (Kaggle)"
        )
        st.caption("Values are taken from the training log of this model.")


# ---------------- layout ----------------
st.sidebar.title("🧠 Brain Tumor App")
mode = st.sidebar.radio("Choose page", ["🔍 Analyze MRI", "📚 Learn about conditions", "📊 Model performance"])
st.sidebar.divider()
st.sidebar.markdown("**Model:** MobileNetV2")
st.sidebar.markdown("**Validation accuracy:** ~84.8%")
st.sidebar.warning("For educational purposes only. Not a diagnostic tool.")

st.markdown(
    '<div class="hero"><h1>🧠 Brain Tumor Detection App</h1>'
    "<p>Upload an MRI scan, see the prediction with charts, and learn about the condition.</p></div>",
    unsafe_allow_html=True,
)

if mode.startswith("🔍"):
    analyze_page()
elif mode.startswith("📚"):
    learn_page()
else:
    performance_page()
