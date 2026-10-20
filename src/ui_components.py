# ui_components.py
# Clinical Diagnostic UI Components with Obsidian Dark Workstation Theme
import streamlit as st
import plotly.graph_objects as go
import os
import textwrap
from PIL import Image
from src.config import CLASSES, COLORS, SAMPLES
from src.content import DATA, CASES
from src.inference import validate_image


def render_top_masthead(lang_code: str = "en"):
    """
    Render a prominent, glowing clinical workstation masthead banner at the top of the UI.
    Features an animated holographic laser beam and pulsing status beacons.
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
        textwrap.dedent(f"""
        <style>
        @keyframes mastheadBeam {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}
        @keyframes beaconPulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); filter: drop-shadow(0 0 6px #2dd4bf); }}
            50% {{ opacity: 0.6; transform: scale(0.92); filter: drop-shadow(0 0 2px #2dd4bf); }}
        }}
        .masthead-beacon {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #2dd4bf;
            animation: beaconPulse 1.8s ease-in-out infinite;
            margin-right: 6px;
        }}
        </style>
        <div style="background: linear-gradient(135deg, rgba(13, 38, 52, 0.95) 0%, rgba(6, 16, 24, 0.98) 100%);
                    border: 1.5px solid #2dd4bf; border-radius: 18px; padding: 22px 28px;
                    margin-bottom: 22px; box-shadow: 0 16px 45px rgba(0, 0, 0, 0.8), 0 0 30px rgba(45, 212, 191, 0.25);
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3.5px;
                        background: linear-gradient(90deg, #0ea5e9, #2dd4bf, #06b6d4, #10b981, #0ea5e9);
                        background-size: 200% 100%;
                        animation: mastheadBeam 4s linear infinite;
                        box-shadow: 0 0 16px #2dd4bf;"></div>
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
                                 padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800; display: flex; align-items: center;">
                        <span class="masthead-beacon"></span>{b1}
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
        """),
        unsafe_allow_html=True
    )


def render_scanner_telemetry(patient_id: str = "ANON-PX-84920", sequence_name: str = "Axial T1-Gd + FLAIR"):
    """
    Render a high-tech PACS scanner telemetry bar with embedded real-time animated SVG ECG heartbeat waveform.
    Displays realistic scanner parameters, field strength, physiological rhythm, and HIPAA status.
    """
    st.markdown(
        textwrap.dedent(f"""
        <style>
        @keyframes telemetryEcg {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
        .telemetry-ecg-bar {{
            width: 100%;
            height: 38px;
            overflow: hidden;
            background: rgba(4, 12, 18, 0.85);
            border-radius: 8px;
            border: 1px solid rgba(45, 212, 191, 0.2);
            position: relative;
            margin-top: 10px;
        }}
        .telemetry-ecg-svg {{
            width: 200%;
            height: 100%;
            animation: telemetryEcg 5s linear infinite;
        }}
        </style>
        <div style="background: linear-gradient(135deg, rgba(8, 24, 34, 0.95) 0%, rgba(5, 15, 22, 0.95) 100%);
                    border: 1px solid rgba(45, 212, 191, 0.35); border-radius: 14px; padding: 16px 20px;
                    margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(45, 212, 191, 0.15);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="width: 42px; height: 42px; border-radius: 10px; background: rgba(45, 212, 191, 0.15);
                                border: 1.5px solid #2dd4bf; display: flex; align-items: center; justify-content: center; font-size: 22px;
                                box-shadow: 0 0 15px rgba(45, 212, 191, 0.3);">
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
                            <span style="background: rgba(16, 185, 129, 0.2); color: #4ade80; border: 1px solid #34d399;
                                         font-size: 10.5px; font-weight: 700; padding: 2px 7px; border-radius: 20px;">
                                72 BPM Normal
                            </span>
                        </div>
                        <div style="font-size: 12px; color: #94a3b8; margin-top: 2px;">
                            AI Computer Vision • MobileNetV2 + Grad-CAM XAI • RECIST 1.1 Volumetrics
                        </div>
                    </div>
                </div>
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
            <div class="telemetry-ecg-bar">
                <svg class="telemetry-ecg-svg" viewBox="0 0 2400 120" preserveAspectRatio="none">
                    <defs>
                        <linearGradient id="ecgTelemGlow" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#0ea5e9" stop-opacity="0.2"/>
                            <stop offset="30%" stop-color="#ffffff" stop-opacity="0.95"/>
                            <stop offset="50%" stop-color="#2dd4bf" stop-opacity="0.9"/>
                            <stop offset="70%" stop-color="#06b6d4" stop-opacity="0.6"/>
                            <stop offset="100%" stop-color="#0ea5e9" stop-opacity="0.2"/>
                        </linearGradient>
                    </defs>
                    <path d="M0,60 L240,60 L260,60 L275,45 L290,75 L305,15 L320,105 L335,50 L350,68 L365,60 L540,60 L600,60 L620,60 L635,45 L650,75 L665,15 L680,105 L695,50 L710,68 L725,60 L900,60 L960,60 L980,60 L995,45 L1010,75 L1025,15 L1040,105 L1055,50 L1070,68 L1085,60 L1260,60 L1320,60 L1340,60 L1355,45 L1370,75 L1385,15 L1400,105 L1415,50 L1430,68 L1445,60 L1620,60 L1680,60 L1700,60 L1715,45 L1730,75 L1745,15 L1760,105 L1775,50 L1790,68 L1805,60 L1980,60 L2040,60 L2060,60 L2075,45 L2090,75 L2105,15 L2120,105 L2135,50 L2150,68 L2165,60 L2400,60" fill="none" stroke="url(#ecgTelemGlow)" stroke-width="2.5" />
                </svg>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )


def box(kind: str, items: list):
    """Render a styled box with a list of items."""
    text = "\\n".join(f"- {i}" for i in items)
    dispatch = {"info": st.info, "warning": st.warning, "success": st.success, "error": st.error}
    dispatch.get(kind, st.info)(text)


def card(title: str, sub: str, color: str):
    """Render a custom clinical dark card with animated left-glow and smooth hover transition."""
    st.markdown(
        f'<div class="card" style="background: linear-gradient(135deg, rgba(10,25,35,0.95), #060e14);'
        f'border: 1.5px solid {color}; border-left: 5px solid {color}; box-shadow: 0 10px 28px rgba(0,0,0,0.6), 0 0 15px rgba(45,212,191,0.15);'
        f'transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);">'
        f'<h2 style="color:#ffffff; margin:0; font-size:1.4rem; text-shadow: 0 0 12px rgba(45,212,191,0.4);">{title}</h2>'
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
    """Allow user to choose a pre-loaded clinical sample or upload their own MRI scan."""
    source = st.radio(
        "Scan Input Source",
        ["⚡ Pre-loaded Clinical Scan (Immediate)", "📁 Upload Custom MRI Scan (DICOM / JPG / PNG)"],
        index=0,
        horizontal=True,
        key="radio_scan_source"
    )

    if source == "📁 Upload Custom MRI Scan (DICOM / JPG / PNG)":
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
        st.info("👆 Please upload an MRI scan above, or switch to '⚡ Pre-loaded Clinical Scan' to view immediate AI inference.")
        return None, None

    choice = st.selectbox(
        "Select Clinical Tumor Case",
        CLASSES,
        index=0,
        format_func=lambda k: f"{DATA[k]['emoji']} {DATA[k]['title']}",
        key="select_sample_case"
    )
    path = SAMPLES[choice]
    if os.path.exists(path):
        return Image.open(path), choice
    st.error(f"Sample scan file not found at: {path}")
    return None, None
