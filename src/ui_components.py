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
        b1 = "01 —— 3.0T एमआरआई कैलिब्रेटेड"
        b2 = "02 —— एफडीए एसएएमडी क्लास II"
        b3 = "03 —— HL7 / FHIR R4 मानक"
        b4 = "04 —— HIPAA सुरक्षित"
    else:
        app_name = "🧠 NEUROSCAN PACS"
        app_sub = "CLINICAL NEURO-ONCOLOGY DECISION SUPPORT WORKSTATION"
        b1 = "01 —— 3.0T MRI Calibrated"
        b2 = "02 —— FDA SaMD Class II"
        b3 = "03 —— HL7 / FHIR R4 Standard"
        b4 = "04 —— HIPAA Safe Harbor Enforced"

    st.markdown(
        textwrap.dedent(f"""
        <style>
        @keyframes mastheadBeam {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}
        @keyframes beaconPulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); filter: drop-shadow(0 0 6px #0EA5E9); }}
            50% {{ opacity: 0.5; transform: scale(0.9); filter: drop-shadow(0 0 2px #0EA5E9); }}
        }}
        .masthead-beacon {{
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #0EA5E9;
            animation: beaconPulse 1.8s ease-in-out infinite;
            margin-right: 6px;
        }}
        </style>
        <div style="background: linear-gradient(135deg, #0E1726 0%, #090D16 100%);
                    border: 1.5px solid rgba(56, 189, 248, 0.25); border-radius: 14px; padding: 20px 24px;
                    margin-bottom: 20px; box-shadow: 0 14px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(14, 165, 233, 0.12);
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px;
                        background: linear-gradient(90deg, #0284C7, #0EA5E9, #38BDF8, #0EA5E9, #0284C7);
                        background-size: 200% 100%;
                        animation: mastheadBeam 4s linear infinite;
                        box-shadow: 0 0 12px #0EA5E9;"></div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
                <div>
                    <h1 style="font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 26px; font-weight: 800; color: #ffffff; margin: 0;
                               letter-spacing: -0.3px; text-shadow: 0 0 16px rgba(14, 165, 233, 0.3);
                               display: flex; align-items: center; gap: 10px;">
                        <span>{app_name}</span>
                    </h1>
                    <div style="font-size: 11.5px; font-weight: 700; color: #38BDF8; margin-top: 4px; letter-spacing: 1.2px; text-transform: uppercase;">
                        {app_sub}
                    </div>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    <span style="background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); color: #38BDF8;
                                 padding: 4px 11px; border-radius: 8px; font-size: 11px; font-weight: 700; display: flex; align-items: center;">
                        <span class="masthead-beacon"></span>{b1}
                    </span>
                    <span style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(56, 189, 248, 0.2); color: #E2E8F0;
                                 padding: 4px 11px; border-radius: 8px; font-size: 11px; font-weight: 700;">
                        {b2}
                    </span>
                    <span style="background: rgba(14, 165, 233, 0.12); border: 1px solid rgba(56, 189, 248, 0.25); color: #E2E8F0;
                                 padding: 4px 11px; border-radius: 8px; font-size: 11px; font-weight: 700;">
                        {b3}
                    </span>
                    <span style="background: rgba(15, 23, 42, 0.95); border: 1.5px solid #10B981; color: #34D399;
                                 padding: 4px 11px; border-radius: 8px; font-size: 11px; font-weight: 700; box-shadow: 0 0 10px rgba(16, 185, 129, 0.25);">
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
    Render high-precision PACS scanner telemetry bar with clinical laser animations.
    Displays realistic scanner parameters, field strength, physiological status, and HIPAA security.
    """
    st.markdown(
        textwrap.dedent(f"""
        <style>
        @keyframes telemetryLaser {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}
        @keyframes radarPingGreen {{
            0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}
        @keyframes radarPingCyan {{
            0% {{ box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.7); }}
            70% {{ box-shadow: 0 0 0 6px rgba(14, 165, 233, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(14, 165, 233, 0); }}
        }}
        @keyframes iconBreathGlow {{
            0%, 100% {{ box-shadow: 0 0 10px rgba(14, 165, 233, 0.3); border-color: #0EA5E9; }}
            50% {{ box-shadow: 0 0 20px rgba(56, 189, 248, 0.65); border-color: #38BDF8; }}
        }}
        .status-beacon-green {{
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #10B981;
            margin-right: 5px;
            animation: radarPingGreen 1.8s infinite;
        }}
        .status-beacon-cyan {{
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #0EA5E9;
            margin-right: 5px;
            animation: radarPingCyan 2s infinite;
        }}
        .icon-workstation-pulse {{
            animation: iconBreathGlow 3s ease-in-out infinite;
        }}
        </style>
        <div style="background: linear-gradient(135deg, #0E1726 0%, #090D16 100%);
                    border: 1.5px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 16px 20px;
                    margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 15px rgba(14, 165, 233, 0.1);
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px;
                        background: linear-gradient(90deg, transparent, #0EA5E9, #38BDF8, #0EA5E9, transparent);
                        background-size: 200% 100%;
                        animation: telemetryLaser 4.5s linear infinite;
                        box-shadow: 0 0 8px #0EA5E9;"></div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div class="icon-workstation-pulse"
                         style="width: 42px; height: 42px; border-radius: 10px; background: #090D16;
                                border: 1.5px solid #0EA5E9; display: flex; align-items: center; justify-content: center; font-size: 22px;">
                        🧠
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                            <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 17.5px; font-weight: 800; color: #ffffff; letter-spacing: -0.2px;">
                                NeuroScan PACS Diagnostic Workstation
                            </span>
                            <span style="background: rgba(14, 165, 233, 0.18); color: #38BDF8; border: 1px solid #0EA5E9;
                                         font-size: 10.5px; font-weight: 800; padding: 2px 8px; border-radius: 6px; display: inline-flex; align-items: center;">
                                <span class="status-beacon-cyan"></span>3.0T MRI
                            </span>
                            <span style="background: rgba(16, 185, 129, 0.18); color: #34D399; border: 1px solid #10B981;
                                         font-size: 10.5px; font-weight: 700; padding: 2px 8px; border-radius: 6px; display: inline-flex; align-items: center;">
                                <span class="status-beacon-green"></span>72 BPM Normal
                            </span>
                        </div>
                        <div style="font-size: 11.5px; color: #94A3B8; margin-top: 3px; letter-spacing: 0.3px;">
                            AI Computer Vision • MobileNetV2 + Grad-CAM XAI • RECIST 1.1 Volumetrics
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 16px; align-items: center; flex-wrap: wrap;">
                    <div style="border-left: 1px solid rgba(56, 189, 248, 0.2); padding-left: 14px;">
                        <div style="font-size: 10px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px;">Patient Token</div>
                        <div style="font-size: 12.5px; font-weight: 700; color: #38BDF8; font-family: monospace;">{patient_id}</div>
                    </div>
                    <div style="border-left: 1px solid rgba(56, 189, 248, 0.2); padding-left: 14px;">
                        <div style="font-size: 10px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px;">Active Protocol</div>
                        <div style="font-size: 12px; font-weight: 600; color: #F1F5F9;">{sequence_name}</div>
                    </div>
                    <div style="border-left: 1px solid rgba(56, 189, 248, 0.2); padding-left: 14px;">
                        <div style="font-size: 10px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px;">HIPAA Security</div>
                        <div style="font-size: 11.5px; font-weight: 700; color: #10B981; display: flex; align-items: center;">
                            <span class="status-beacon-green"></span>Safe Harbor Active
                        </div>
                    </div>
                </div>
            </div>
            <!-- Clean Clinical Parameter Ribbon (No Wave) -->
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(56, 189, 248, 0.15);
                        display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;
                        font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94A3B8;">
                <div><span style="color: #38BDF8; font-weight: 700;">SCANNER:</span> MAGNETOM Skyra 3.0T</div>
                <div><span style="color: #38BDF8; font-weight: 700;">COIL:</span> 64-Ch Neuro Matrix</div>
                <div><span style="color: #38BDF8; font-weight: 700;">VOXEL:</span> 0.8 × 0.8 × 1.0 mm³</div>
                <div><span style="color: #38BDF8; font-weight: 700;">SLICES:</span> 176 Axial</div>
                <div><span style="color: #10B981; font-weight: 700;">● RECON:</span> Deep Resolve AI</div>
                <div><span style="color: #38BDF8; font-weight: 700;">ARCHIVE:</span> PACS / DICOM 3.0</div>
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
    """Render a custom clinical dark card with clean surgical styling and laser glow accent."""
    st.markdown(
        f'<div class="card" style="background: linear-gradient(135deg, #0E1726 0%, #090D16 100%);'
        f'border: 1.5px solid {color}; border-left: 5px solid {color}; border-radius: 12px; padding: 18px 20px;'
        f'margin-bottom: 14px; position: relative; overflow: hidden;'
        f'box-shadow: 0 10px 28px rgba(0,0,0,0.8), 0 0 15px rgba(14,165,233,0.12);'
        f'transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);">'
        f'<div style="position: absolute; top: 0; left: 0; right: 0; height: 1.5px;'
        f'background: linear-gradient(90deg, transparent, {color}, transparent); opacity: 0.8;"></div>'
        f'<h2 style="font-family: \'Plus Jakarta Sans\', sans-serif; color:#ffffff; margin:0; font-size:1.35rem; font-weight:700;">{title}</h2>'
        f'<p style="color:#94A3B8; margin:6px 0 0 0; font-size:1.02rem;">{sub}</p></div>',
        unsafe_allow_html=True,
    )


def style(fig, height: int = 300):
    """Apply consistent clinical dark styling to plotly figures."""
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", family="Plus Jakarta Sans, sans-serif"),
        xaxis=dict(gridcolor="rgba(168, 85, 247, 0.15)"),
        yaxis=dict(gridcolor="rgba(168, 85, 247, 0.15)")
    )
    return fig


def gauge(conf: float, color: str):
    """Render a dark clinical gauge chart for confidence."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=conf,
        number={"suffix": "%", "font": {"color": "#ffffff", "size": 36}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#A5B4FC", "tickfont": {"color": "#A5B4FC"}},
            "bar": {"color": color, "thickness": 0.28},
            "steps": [
                {"range": [0, 50], "color": "rgba(239, 68, 68, 0.25)"},
                {"range": [50, 70], "color": "rgba(245, 158, 11, 0.25)"},
                {"range": [70, 100], "color": "rgba(16, 185, 129, 0.25)"}
            ],
            "threshold": {
                "line": {"color": "#00F5D4", "width": 4},
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
