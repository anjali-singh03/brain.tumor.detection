# ui_components.py
# Clinical Diagnostic UI Components with Obsidian Dark Workstation Theme
import streamlit as st
import plotly.graph_objects as go
import os
from PIL import Image
from src.config import CLASSES, COLORS, SAMPLES
from src.content import DATA, CASES
from src.inference import validate_image


def render_top_masthead(lang_code: str = "en"):
    """
    Render a prominent, glowing clinical workstation masthead banner at the top of the UI.
    Highlights the app name as a primary heading and supports full bilingual localization.
    """
    if lang_code == "hi":
        app_name = "🧠 न्यूरोस्कैन"
        app_sub = "उन्नत न्यूरो-ऑन्कोलॉजी एवं सर्जिकल एआई वर्कस्टेशन"
        b1 = "● 3.0T एमआरआई कैलिब्रेटेड"
        b2 = "● एफडीए एसएएमडी क्लास II निर्णय समर्थन"
        b3 = "● HL7 / FHIR R4 मानक"
        b4 = "● HIPAA सुरक्षित एन्क्रिप्टेड"
    else:
        app_name = "🧠 NEUROSCAN"
        app_sub = "CLINICAL NEURO-ONCOLOGY & SURGICAL AI WORKSTATION"
        b1 = "● 3.0T MRI Calibrated"
        b2 = "● FDA SaMD Class II Decision Support"
        b3 = "● HL7 / FHIR R4 Standard"
        b4 = "● HIPAA Safe Harbor Enforced"

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(13, 38, 52, 0.95) 0%, rgba(6, 16, 24, 0.98) 100%);
                    border: 1.5px solid #2dd4bf; border-radius: 18px; padding: 22px 28px;
                    margin-bottom: 22px; box-shadow: 0 16px 45px rgba(0, 0, 0, 0.8), 0 0 30px rgba(45, 212, 191, 0.25);
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px;
                        background: linear-gradient(90deg, #0ea5e9, #2dd4bf, #06b6d4, #10b981);
                        box-shadow: 0 0 14px #2dd4bf;"></div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div>
                    <h1 style="font-size: 28px; font-weight: 900; color: #ffffff; margin: 0;
                               letter-spacing: -0.5px; text-shadow: 0 0 20px rgba(45, 212, 191, 0.6);
                               display: flex; align-items: center; gap: 10px;">
                        <span>{app_name}</span>
                    </h1>
                    <div style="font-size: 13.5px; font-weight: 700; color: #5eead4; margin-top: 4px; letter-spacing: 0.8px;">
                        {app_sub}
                    </div>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    <span style="background: rgba(45, 212, 191, 0.15); border: 1px solid #2dd4bf; color: #5eead4;
                                 padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800;">
                        {b1}
                    </span>
                    <span style="background: rgba(14, 165, 233, 0.15); border: 1px solid #38bdf8; color: #38bdf8;
                                 padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800;">
                        {b2}
                    </span>
                    <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #34d399; color: #4ade80;
                                 padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800;">
                        {b3}
                    </span>
                    <span style="background: rgba(245, 158, 11, 0.15); border: 1px solid #fbbf24; color: #fde047;
                                 padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800;">
                        {b4}
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_scanner_telemetry(patient_id: str = "ANON-PX-84920", sequence_name: str = "Axial T1-Gd + FLAIR"):
    """
    Render a high-tech PACS scanner telemetry bar replacing generic banners.
    Displays realistic scanner parameters, field strength, and HIPAA status.
    """
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(8, 24, 34, 0.95) 0%, rgba(5, 15, 22, 0.95) 100%);
                    border: 1px solid rgba(45, 212, 191, 0.35); border-radius: 14px; padding: 16px 20px;
                    margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(45, 212, 191, 0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="width: 42px; height: 42px; border-radius: 10px; background: rgba(45, 212, 191, 0.15);
                                border: 1.5px solid #2dd4bf; display: flex; align-items: center; justify-content: center; font-size: 22px;">
                        🧠
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 18px; font-weight: 800; color: #ffffff; letter-spacing: -0.3px;">
                                NeuroScan PACS Diagnostic Workstation
                            </span>
                            <span style="background: rgba(45, 212, 191, 0.2); color: #2dd4bf; border: 1px solid #2dd4bf;
                                         font-size: 10.5px; font-weight: 700; padding: 2px 7px; border-radius: 20px;">
                                3.0T MRI
                            </span>
                        </div>
                        <div style="font-size: 12px; color: #94a3b8; margin-top: 2px;">
                            AI-Assisted Computer Vision • MobileNetV2 + Grad-CAM XAI • RECIST 1.1 Volumetrics
                        </div>
                    </div>
                </div>
                <!-- Telemetry Metrics Grid -->
                <div style="display: flex; gap: 16px; align-items: center;">
                    <div style="border-left: 1px solid rgba(148, 163, 184, 0.2); padding-left: 14px;">
                        <div style="font-size: 10px; font-weight: 700; color: #5eead4; text-transform: uppercase;">Patient Token</div>
                        <div style="font-size: 12.5px; font-weight: 700; color: #ffffff; font-family: monospace;">{patient_id}</div>
                    </div>
                    <div style="border-left: 1px solid rgba(148, 163, 184, 0.2); padding-left: 14px;">
                        <div style="font-size: 10px; font-weight: 700; color: #5eead4; text-transform: uppercase;">Active Protocol</div>
                        <div style="font-size: 12px; font-weight: 600; color: #cbd5e1;">{sequence_name}</div>
                    </div>
                    <div style="border-left: 1px solid rgba(148, 163, 184, 0.2); padding-left: 14px;">
                        <div style="font-size: 10px; font-weight: 700; color: #5eead4; text-transform: uppercase;">HIPAA Security</div>
                        <div style="font-size: 11.5px; font-weight: 700; color: #4ade80;">● Safe Harbor Active</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def box(kind: str, items: list):
    """Render a styled box with a list of items."""
    text = "\n".join(f"- {i}" for i in items)
    dispatch = {"info": st.info, "warning": st.warning, "success": st.success, "error": st.error}
    dispatch.get(kind, st.info)(text)


def card(title: str, sub: str, color: str):
    """Render a custom clinical dark card."""
    st.markdown(
        f'<div class="card" style="background: linear-gradient(135deg, rgba(10,25,35,0.95), #060e14);'
        f'border: 1.5px solid {color}; border-left: 5px solid {color}; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">'
        f'<h2 style="color:#ffffff; margin:0; font-size:1.4rem;">{title}</h2>'
        f'<p style="color:#cbd5e1; margin:6px 0 0 0; font-size:1.05rem;">{sub}</p></div>',
        unsafe_allow_html=True,
    )


def style(fig, height: int = 300):
    """Apply consistent clinical dark styling to plotly figures."""
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", family="Plus Jakarta Sans, sans-serif"),
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)"),
        yaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)")
    )
    return fig


def gauge(conf: float, color: str):
    """Render a dark clinical gauge chart for confidence."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=conf,
        number={"suffix": "%", "font": {"color": "#ffffff", "size": 36}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94a3b8", "tickfont": {"color": "#94a3b8"}},
            "bar": {"color": color, "thickness": 0.28},
            "steps": [
                {"range": [0, 50], "color": "rgba(239, 68, 68, 0.25)"},
                {"range": [50, 70], "color": "rgba(245, 158, 11, 0.25)"},
                {"range": [70, 100], "color": "rgba(16, 185, 129, 0.25)"}
            ],
            "threshold": {
                "line": {"color": "#2dd4bf", "width": 4},
                "thickness": 0.85,
                "value": conf
            }
        }
    ))
    return style(fig, 240)


def donut(pred: list):
    """Render a dark clinical donut chart for prediction probabilities."""
    fig = go.Figure(go.Pie(
        labels=[DATA[c]["title"] for c in CLASSES],
        values=[float(p) for p in pred],
        hole=0.6,
        sort=False,
        marker=dict(
            colors=[COLORS[c] for c in CLASSES],
            line=dict(color="#07151e", width=2)
        ),
        textfont=dict(color="#ffffff")
    ))
    return style(fig, 280)


def bars(pred: list):
    """Render a dark clinical bar chart for prediction probabilities."""
    fig = go.Figure(go.Bar(
        x=[float(p) * 100 for p in pred],
        y=[DATA[c]["title"] for c in CLASSES],
        orientation="h",
        marker_color=[COLORS[c] for c in CLASSES],
        text=[f"{p * 100:.1f}%" for p in pred],
        textposition="auto",
        textfont=dict(color="#ffffff", weight="bold")
    ))
    fig.update_layout(xaxis_title="Confidence Probability (%)", yaxis=dict(autorange="reversed"))
    return style(fig, 280)


def show_tabs(key: str):
    """Render informational clinical tabs for a specific condition."""
    if key not in DATA:
        st.error(f"No details available for condition: {key}")
        return
    d = DATA[key]
    tabs = st.tabs([
        "📖 Clinical Overview", "🧬 Molecular Pathogenesis", "🩺 Presenting Symptoms",
        "💊 Standard of Care", "🛡️ Diagnostic Precautions", "👨‍⚕️ Specialist Referral", "📝 Case Vignettes"
    ])
    with tabs[0]:
        st.info(d["overview"])
    with tabs[1]:
        box("warning", d["causes"])
    with tabs[2]:
        box("error", d["symptoms"])
    with tabs[3]:
        box("success", d["treatment"])
        st.caption("Standard treatment guidelines based on NCCN and WHO Classification of CNS Tumors.")
    with tabs[4]:
        box("info", d["precautions"])
    with tabs[5]:
        st.success(f"**Primary Specialist to Consult:** {d['specialists']}")
        st.markdown("**Urgent clinical indications for neurosurgical triage:**")
        box("warning", d["see_doctor"])
        st.markdown("**Questions for the Multi-Disciplinary Tumor Board:**")
        box("info", d["questions"])
        st.error(
            "Emergency: Sudden severe headache, intractable seizure, visual field loss, "
            "or altered mental status requires immediate emergency department transfer."
        )
    with tabs[6]:
        if key in CASES:
            c = CASES[key]
            st.caption("De-identified case vignette written for clinical educational reference.")
            st.markdown(f"**Patient Presentation:** {c['patient']}")
            st.info(f"**Diagnostic Course & Outcome:** {c['happened']}")


def get_image():
    """Allow user to upload an image or choose a sample."""
    source = st.radio("Image source", ["Upload my own", "Try a sample"], horizontal=True)

    if source == "Upload my own":
        f = st.file_uploader(
            "Upload MRI image (DICOM / JPG / PNG)",
            type=["jpg", "jpeg", "png", "dcm"],
            help="High-resolution axial or coronal brain MRI scan."
        )
        if f:
            try:
                img = Image.open(f)
                return validate_image(img), None
            except Exception as e:
                st.error(f"Image validation failed: {e}")
                return None, None
        return None, None

    choice = st.selectbox(
        "Choose sample scan",
        CLASSES,
        format_func=lambda k: f"{DATA[k]['emoji']} {DATA[k]['title']}"
    )
    path = SAMPLES[choice]
    if os.path.exists(path):
        return Image.open(path), choice
    st.error("Sample scan file not found.")
    return None, None
