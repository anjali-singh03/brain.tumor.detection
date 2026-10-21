import sys
import importlib

# Ensure in-memory custom modules are automatically synced on hot-reloads
for _mod in ["src.inference", "src.ui_components", "src.pacs", "src.neuro_copilot", "src.report_generator", "src.auth", "src.fhir_exporter"]:
    if _mod in sys.modules:
        importlib.reload(sys.modules[_mod])

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os
import tempfile
import json
from PIL import Image

from src.config import CLASSES, COLORS, SAMPLES, MODEL_PATH
from src.content import DATA
from src.inference import (
    load_model, preprocess_image, predict,
    get_gradcam_heatmap, overlay_gradcam, validate_image,
    PRECOMPUTED_SAMPLE_INFERENCE
)
from src.ui_components import (
    card, style, gauge, donut, bars, show_tabs, get_image,
    render_scanner_telemetry, render_top_masthead
)
from src.utils import get_logger, setup_app_state
from src.report_generator import create_pdf_report
from src.auth import is_authenticated, render_login_page, render_user_profile_sidebar, get_current_user
from src.pacs import (
    adjust_window_level, simulate_mri_sequences, compute_recist_metrics,
    generate_dicom_telemetry, extract_tumor_contours
)
from src.fhir_exporter import generate_fhir_diagnostic_report
from src.neuro_copilot import (
    calculate_surgical_risk, render_risk_radar, render_survival_trajectory
)

logger = get_logger(__name__)

st.set_page_config(
    page_title="NeuroScan PACS — Clinical Brain Tumor Diagnostics",
    page_icon="🧠",
    layout="wide"
)
setup_app_state(st)

# Authentication Guard: Enforce modern login screen if user is unauthenticated
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not is_authenticated():
    render_login_page()
    st.stop()

# Initialize Global Language Session State
if "lang_code" not in st.session_state:
    st.session_state["lang_code"] = "en"

# Clinical Workstation Stylesheet with New Palette (#2A2539, #353044, #5E5373, #DBD8E3)
st.markdown(
    """
<style>
/* Base Theme Canvas */
.stApp {
    background-color: #2A2539 !important;
    background: radial-gradient(circle at 50% 12%, #353044 0%, #2A2539 50%, #1c1827 100%) !important;
    color: #DBD8E3 !important;
    min-height: 100vh !important;
    height: 100vh !important;
}

.stAppViewContainer, [data-testid="stAppViewContainer"] {
    min-height: 100vh !important;
    height: 100% !important;
}

/* Ambient Horizon Dome Animation with Soft Lilac Glow */
.ambient-horizon-main {
    position: fixed;
    bottom: -280px;
    left: 50%;
    transform: translateX(-50%);
    width: 900px;
    height: 520px;
    border-radius: 50%;
    background: radial-gradient(circle at 50% 20%, rgba(94, 83, 115, 0.4) 0%, rgba(53, 48, 68, 0.15) 45%, transparent 75%);
    pointer-events: none;
    filter: blur(14px);
    z-index: 0;
    animation: horizonGlow 7s ease-in-out infinite alternate;
}

@keyframes horizonGlow {
    0% { opacity: 0.6; transform: translateX(-50%) scale(0.96); }
    100% { opacity: 1; transform: translateX(-50%) scale(1.04); }
}

/* Global Bottom Animated ECG Pulse Ticker */
.global-ecg-ticker {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 32px;
    background: rgba(42, 37, 57, 0.95);
    backdrop-filter: blur(8px);
    border-top: 1px solid rgba(219, 216, 227, 0.2);
    z-index: 999;
    overflow: hidden;
    pointer-events: none;
}

.global-ecg-svg {
    width: 200%;
    height: 100%;
    animation: ecgFlow 6s linear infinite;
}

@keyframes ecgFlow {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* Highlighted Sidebar Clinical Navigation */
.nav-header-pill {
    background: rgba(94, 83, 115, 0.35);
    border: 1px solid #8E82A6;
    color: #DBD8E3;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    display: inline-block;
    margin-bottom: 12px;
    box-shadow: 0 0 12px rgba(94, 83, 115, 0.3);
}

div[data-testid="stRadio"] > div {
    gap: 8px !important;
}

div[data-testid="stRadio"] label {
    background: rgba(53, 48, 68, 0.85) !important;
    border: 1px solid rgba(219, 216, 227, 0.15) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    cursor: pointer !important;
}

div[data-testid="stRadio"] label:hover {
    border-color: #DBD8E3 !important;
    background: rgba(94, 83, 115, 0.45) !important;
    transform: translateX(6px) !important;
    box-shadow: 0 6px 20px rgba(94, 83, 115, 0.35) !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, rgba(94, 83, 115, 0.75) 0%, rgba(53, 48, 68, 0.95) 100%) !important;
    border: 1.5px solid #DBD8E3 !important;
    box-shadow: 0 0 20px rgba(94, 83, 115, 0.5) !important;
    transform: translateX(4px) !important;
}

div[data-testid="stRadio"] label span p {
    font-size: 13.5px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: 0.2px !important;
}

/* Card Styling with Interactive Elevation */
.card {
    padding: 20px;
    border-radius: 14px;
    color: #DBD8E3;
    margin-bottom: 14px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.card:hover {
    transform: translateY(-4px) scale(1.006);
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.8), 0 0 24px rgba(94, 83, 115, 0.3);
}

/* DICOM Inspector Box */
.dicom-box {
    background: #2A2539;
    border: 1px solid rgba(219, 216, 227, 0.25);
    border-radius: 10px;
    padding: 12px 16px;
    font-family: monospace;
    font-size: 12px;
    color: #DBD8E3;
    margin-bottom: 14px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
}

/* Streamlit Tabs Dark Styling with Glowing Indicator */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(42, 37, 57, 0.9);
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(219, 216, 227, 0.2);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    color: #a49cb5;
    font-weight: 700;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #DBD8E3;
    background-color: rgba(94, 83, 115, 0.2);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(94, 83, 115, 0.6) 0%, rgba(53, 48, 68, 0.85) 100%) !important;
    border: 1px solid #DBD8E3 !important;
    color: #ffffff !important;
    box-shadow: 0 0 14px rgba(94, 83, 115, 0.4) !important;
}

/* Animated Scanline on MRI Viewports */
div[data-testid="stImage"] {
    position: relative !important;
    border: 2px solid rgba(94, 83, 115, 0.6) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.7), 0 0 20px rgba(94, 83, 115, 0.25) !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stImage"]:hover {
    border-color: #DBD8E3 !important;
    box-shadow: 0 16px 45px rgba(0, 0, 0, 0.85), 0 0 35px rgba(94, 83, 115, 0.45) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stImage"]::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #DBD8E3, #8E82A6, #DBD8E3, transparent);
    box-shadow: 0 0 12px #DBD8E3, 0 0 22px #8E82A6;
    z-index: 5;
    pointer-events: none;
    animation: laserScan 4s ease-in-out infinite alternate;
}

/* Animated Laser Scanner Viewport Frame */
.mri-viewport-container {
    position: relative;
    border: 2px solid rgba(94, 83, 115, 0.5);
    border-radius: 16px;
    overflow: hidden;
    background: #1B1726;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.8), 0 0 25px rgba(94, 83, 115, 0.3);
}

.laser-scan-bar {
    position: absolute;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #DBD8E3, #8E82A6, #DBD8E3, transparent);
    box-shadow: 0 0 14px #DBD8E3, 0 0 24px #8E82A6;
    z-index: 5;
    pointer-events: none;
    animation: laserScan 3.5s ease-in-out infinite alternate;
}

@keyframes laserScan {
    0% { top: 2%; opacity: 0.9; }
    50% { opacity: 1; }
    100% { top: 96%; opacity: 0.85; }
}

/* Primary Action Buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #5E5373 0%, #3e364f 100%) !important;
    color: #ffffff !important;
    border: 1px solid #DBD8E3 !important;
    border-radius: 20px !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 18px rgba(94, 83, 115, 0.5) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 26px rgba(219, 216, 227, 0.6) !important;
    transform: translateY(-2px) scale(1.01) !important;
}

/* Preset Buttons */
.preset-btn {
    display: inline-block;
    padding: 4px 10px;
    background: rgba(94, 83, 115, 0.35);
    border: 1px solid #8E82A6;
    border-radius: 12px;
    color: #DBD8E3;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
}
.preset-btn:hover {
    background: #5E5373;
    border-color: #DBD8E3;
    color: #ffffff;
}
</style>

<!-- Ambient Glowing Horizon Dome -->
<div class="ambient-horizon-main"></div>

<!-- Global Animated SVG ECG Rhythm Ticker -->
<div class="global-ecg-ticker">
    <svg class="global-ecg-svg" viewBox="0 0 2400 120" preserveAspectRatio="none">
        <defs>
            <linearGradient id="ecgGlobalGlow" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#5E5373" stop-opacity="0.2"/>
                <stop offset="30%" stop-color="#ffffff" stop-opacity="0.95"/>
                <stop offset="50%" stop-color="#DBD8E3" stop-opacity="0.9"/>
                <stop offset="70%" stop-color="#8E82A6" stop-opacity="0.7"/>
                <stop offset="100%" stop-color="#5E5373" stop-opacity="0.2"/>
            </linearGradient>
        </defs>
        <path d="
            M0,60 L240,60 L260,60 L275,45 L290,75 L305,15 L320,105 L335,50 L350,68 L365,60 L540,60
            L600,60 L620,60 L635,45 L650,75 L665,15 L680,105 L695,50 L710,68 L725,60 L900,60
            L960,60 L980,60 L995,45 L1010,75 L1025,15 L1040,105 L1055,50 L1070,68 L1085,60 L1260,60
            L1320,60 L1340,60 L1355,45 L1370,75 L1385,15 L1400,105 L1415,50 L1430,68 L1445,60 L1620,60
            L1680,60 L1700,60 L1715,45 L1730,75 L1745,15 L1760,105 L1775,50 L1790,68 L1805,60 L1980,60
            L2040,60 L2060,60 L2075,45 L2090,75 L2105,15 L2120,105 L2135,50 L2150,68 L2165,60 L2400,60
        " fill="none" stroke="url(#ecgGlobalGlow)" stroke-width="2.2" />
    </svg>
</div>
""",
    unsafe_allow_html=True,
)

# Comprehensive Multi-Language Dictionary
I18N = {
    "en": {
        "nav_title": "CLINICAL NAVIGATION",
        "nav_pacs": "🔍 PACS Diagnostics & AI",
        "nav_copilot": "🧠 NeuroCopilot™ AI Surgical Risk",
        "nav_board": "📈 Longitudinal Tumor Board",
        "nav_batch": "📁 Batch Upload & Triage",
        "nav_compare": "⚖️ Compare Scans",
        "nav_library": "📚 Condition Library",
        "nav_safety": "📊 Safety & Validation Metrics",
        "pacs_processing": "🎛️ PACS Image Processing",
        "win_level": "Window Level (Brightness)",
        "win_width": "Window Width (Contrast)",
        "clahe": "CLAHE Soft-Tissue",
        "clahe_help": "Contrast Limited Adaptive Histogram Equalization",
        "invert": "Invert Negative",
        "invert_help": "Enhances subtle calcifications and bone margins",
        "caliper_header": "📏 Caliper & RECIST Staging",
        "tumor_max_diam": "Tumor Max Diameter (mm)",
        "perp_width": "Perpendicular Width (mm)",
        "diag_threshold": "Diagnostic Threshold (%)",
        "upload_or_sample": "👆 Upload an MRI scan (DICOM / JPG / PNG) or select a clinical sample below.",
        "analyzing": "Running Deep ConvNet & Grad-CAM XAI Inference...",
        "gradcam_opacity": "Grad-CAM AI Focus Opacity",
        "tab_gradcam": "🔥 Grad-CAM Focus",
        "tab_contours": "🎯 Core vs Edema Contours",
        "tab_dicom": "📋 DICOM Metadata",
        "est_volume": "Estimated Volume",
        "max_diam": "Max Axial Diameter",
        "mass_effect": "Mass Effect",
        "prob_distribution": "📈 Neural Probability Distribution",
        "dictation_header": "🎙️ Radiologist Dictation & Clinical Notes",
        "dictation_caption": "Dictate or type clinical impression to be integrated into the official EHR report.",
        "guidelines_header": "📑 Condition Clinical Guidelines",
        "export_header": "📥 Export Official Clinical Reports",
        "download_pdf": "⬇️ Download Clinical PDF Report",
        "download_fhir": "📋 Export HL7 / FHIR R4 JSON",
        "uncertain": "❓ High Uncertainty: Equivocal Finding - Multidisciplinary Review Advised",
        "low_conf": "Low confidence probability. Secondary diagnostic confirmation mandatory."
    },
    "hi": {
        "nav_title": "क्लिनिकल नेविगेशन",
        "nav_pacs": "🔍 पैक्स निदान एवं एआई",
        "nav_copilot": "🧠 न्यूरोकॉपायलट™ सर्जिकल जोखिम",
        "nav_board": "📈 दीर्घकालिक ट्यूमर बोर्ड",
        "nav_batch": "📁 बैच अपलोड व प्राथमिकता",
        "nav_compare": "⚖️ स्कैन की तुलना करें",
        "nav_library": "📚 बीमारी संदर्भ पुस्तकालय",
        "nav_safety": "📊 सुरक्षा और सत्यापन मेट्रिक्स",
        "pacs_processing": "🎛️ पैक्स छवि प्रसंस्करण",
        "win_level": "विंडो स्तर (चमक)",
        "win_width": "विंडो चौड़ाई (कंट्रास्ट)",
        "clahe": "CLAHE कोमल-ऊतक संवर्धन",
        "clahe_help": "सूक्ष्म ऊतकों के कंट्रास्ट को बढ़ाता है",
        "invert": "नेगेटिव इनवर्ट करें",
        "invert_help": "हड्डियों व कैल्सीफिकेशन को स्पष्ट करता है",
        "caliper_header": "📏 कैलिपर और रेसिस्ट स्टेजिंग",
        "tumor_max_diam": "ट्यूमर अधिकतम व्यास (मिमी)",
        "perp_width": "लंबवत चौड़ाई (मिमी)",
        "diag_threshold": "नैदानिक सीमा (%)",
        "upload_or_sample": "👆 एमआरआई स्कैन अपलोड करें या नीचे दिए गए क्लिनिकल नमूने चुनें।",
        "analyzing": "गहरा तंत्रिका विश्लेषण व Grad-CAM हीटमैप तैयार हो रहा है...",
        "gradcam_opacity": "Grad-CAM एआई फोकस दृश्यता",
        "tab_gradcam": "🔥 Grad-CAM फोकस",
        "tab_contours": "🎯 कोर बनाम एडिमा सीमा",
        "tab_dicom": "📋 DICOM मेटाडेटा",
        "est_volume": "अनुमानित आयतन",
        "max_diam": "अधिकतम अक्षीय व्यास",
        "mass_effect": "द्रव्यमान प्रभाव",
        "prob_distribution": "📈 तंत्रिका संभावना वितरण",
        "dictation_header": "🎙️ रेडियोलॉजिस्ट डिक्टेशन व नोट्स",
        "dictation_caption": "आधिकारिक अस्पताल रिपोर्ट के लिए अपने क्लिनिकल निष्कर्ष दर्ज करें।",
        "guidelines_header": "📑 बीमारी के क्लिनिकल दिशानिर्देश",
        "export_header": "📥 आधिकारिक क्लिनिकल रिपोर्ट निर्यात",
        "download_pdf": "⬇️ क्लिनिकल पीडीएफ रिपोर्ट डाउनलोड करें",
        "download_fhir": "📋 HL7 / FHIR R4 JSON निर्यात करें",
        "uncertain": "❓ उच्च अनिश्चितता: विशेषज्ञ समीक्षा की सलाह दी जाती है",
        "low_conf": "कम आत्मविश्वास। द्वितीयक पुष्टि अनिवार्य है।"
    }
}


# ---------------- SIDEBAR NAVIGATION & LANGUAGE ----------------
render_user_profile_sidebar()

# Prominent Clinical Workstation Navigation Section
st.sidebar.markdown(f'<div class="nav-header-pill">● {I18N[st.session_state["lang_code"]]["nav_title"]}</div>', unsafe_allow_html=True)

nav_options_en = [
    "🔍 PACS Diagnostics & AI",
    "🧠 NeuroCopilot™ AI Surgical Risk",
    "📈 Longitudinal Tumor Board",
    "📁 Batch Upload & Triage",
    "⚖️ Compare Scans",
    "📚 Condition Library",
    "📊 Safety & Validation Metrics"
]

nav_options_hi = [
    "🔍 पैक्स निदान एवं एआई",
    "🧠 न्यूरोकॉपायलट™ सर्जिकल जोखिम",
    "📈 दीर्घकालिक ट्यूमर बोर्ड",
    "📁 बैच अपलोड व प्राथमिकता",
    "⚖️ स्कैन की तुलना करें",
    "📚 बीमारी संदर्भ पुस्तकालय",
    "📊 सुरक्षा और सत्यापन मेट्रिक्स"
]

current_options = nav_options_hi if st.session_state["lang_code"] == "hi" else nav_options_en

selected_nav = st.sidebar.radio(
    "Choose Clinical Module",
    current_options,
    label_visibility="collapsed",
    key="clinical_main_nav"
)

# Map back to standard index for dispatching
nav_idx = current_options.index(selected_nav)

st.sidebar.divider()

# Working Interactive Language Selector
chosen_lang = st.sidebar.selectbox(
    "🌐 System Language / भाषा",
    ["English (US)", "हिंदी (Hindi)"],
    index=0 if st.session_state["lang_code"] == "en" else 1,
    key="global_lang_selector"
)
new_lang_code = "hi" if "Hindi" in chosen_lang else "en"
if new_lang_code != st.session_state["lang_code"]:
    st.session_state["lang_code"] = new_lang_code
    st.rerun()

lang_code = st.session_state["lang_code"]
t = I18N[lang_code]

st.sidebar.divider()
st.sidebar.markdown("**Engine:** MobileNetV2 + Grad-CAM")
st.sidebar.markdown("**Calibration:** Siemens 3.0T MAGNETOM")
st.sidebar.caption("🔒 HIPAA Safe Harbor • FDA SaMD Class II Ready")

# ---------------- RENDER TOP WORKSTATION MASTHEAD ----------------
render_top_masthead(lang_code)


# ---------------- PAGE 1: PACS DIAGNOSTICS & AI ----------------
def analyze_page():
    dicom_info = generate_dicom_telemetry("AX_BRAIN_STUDY.dcm")
    render_scanner_telemetry(patient_id=dicom_info["Patient_Token"], sequence_name="3D T1-Gd MPRAGE + FLAIR")

    col_side, col_main = st.columns([1, 2.5])

    with col_side:
        st.markdown(f"### {t['pacs_processing']}")
        # 1-Click Interactive Window Presets
        st.markdown(
            "<div style='font-size:11px; font-weight:800; color:#DBD8E3; margin-bottom:6px; letter-spacing:0.4px;'>"
            "⚡ 1-CLICK WINDOW PRESETS</div>",
            unsafe_allow_html=True
        )
        pr1, pr2, pr3, pr4 = st.columns(4)
        if "pacs_b" not in st.session_state:
            st.session_state["pacs_b"] = 1.0
        if "pacs_c" not in st.session_state:
            st.session_state["pacs_c"] = 1.0

        with pr1:
            if st.button("🧠 Brain", key="btn_pr_brain", use_container_width=True):
                st.session_state["pacs_b"] = 1.0
                st.session_state["pacs_c"] = 1.0
                st.rerun()
        with pr2:
            if st.button("🩸 Blood", key="btn_pr_blood", use_container_width=True):
                st.session_state["pacs_b"] = 1.25
                st.session_state["pacs_c"] = 1.8
                st.rerun()
        with pr3:
            if st.button("⚡ Stroke", key="btn_pr_stroke", use_container_width=True):
                st.session_state["pacs_b"] = 0.85
                st.session_state["pacs_c"] = 1.6
                st.rerun()
        with pr4:
            if st.button("💀 Bone", key="btn_pr_bone", use_container_width=True):
                st.session_state["pacs_b"] = 1.4
                st.session_state["pacs_c"] = 2.2
                st.rerun()

        brightness = st.slider(t["win_level"], 0.5, 2.0, float(st.session_state.get("pacs_b", 1.0)), 0.05, key="slider_b")
        contrast = st.slider(t["win_width"], 0.5, 2.5, float(st.session_state.get("pacs_c", 1.0)), 0.05, key="slider_c")

        c1, c2 = st.columns(2)
        with c1:
            clahe_on = st.checkbox(t["clahe"], value=False, help=t["clahe_help"])
        with c2:
            invert_on = st.checkbox(t["invert"], value=False, help=t["invert_help"])

        st.markdown("---")
        st.markdown(f"### {t['caliper_header']}")
        caliper_len = st.slider(t["tumor_max_diam"], 0.0, 65.0, 24.5, 0.5)
        caliper_wid = st.slider(t["perp_width"], 0.0, 50.0, 18.2, 0.5)

        threshold = st.slider(t["diag_threshold"], min_value=0, max_value=100, value=70, step=5)

    with col_main:
        img, sample_case = get_image()
        if img is None:
            st.info(t["upload_or_sample"])
            return

        pacs_img = adjust_window_level(
            img, brightness=brightness, contrast=contrast,
            apply_clahe=clahe_on, invert=invert_on
        )

        try:
            x = preprocess_image(img)
        except Exception as e:
            st.error(f"Image preprocessing error: {e}")
            return

        # Instant zero-latency inference cache:
        # Precomputed sample cases and session cache allow PACS sliders to update at 60 FPS without CPU lag
        if "inference_cache" not in st.session_state:
            st.session_state["inference_cache"] = {}

        cache_key = f"sample_{sample_case}" if sample_case else f"custom_{img.size}_{img.mode}"

        if cache_key in st.session_state["inference_cache"]:
            pred, heatmap = st.session_state["inference_cache"][cache_key]
        elif sample_case in PRECOMPUTED_SAMPLE_INFERENCE:
            pred = PRECOMPUTED_SAMPLE_INFERENCE[sample_case]["pred"]
            heatmap = PRECOMPUTED_SAMPLE_INFERENCE[sample_case]["heatmap"]
            st.session_state["inference_cache"][cache_key] = (pred, heatmap)
        else:
            model = load_model(MODEL_PATH)
            if model is None:
                return
            with st.spinner(t["analyzing"]):
                try:
                    pred = predict(model, x)
                    heatmap = get_gradcam_heatmap(model, x)
                    st.session_state["inference_cache"][cache_key] = (pred, heatmap)
                except Exception as e:
                    st.error(f"Error during neural inference: {e}")
                    return

        top_indices = np.argsort(pred)[-2:][::-1]
        idx1, idx2 = top_indices[0], top_indices[1]
        label1 = CLASSES[idx1]
        conf1 = float(pred[idx1]) * 100

        recist_res = compute_recist_metrics(label1, conf1, caliper_len, caliper_wid)
        seq_dict = simulate_mri_sequences(pacs_img)

        st.markdown("#### 🔬 Diagnostic MRI Viewer & AI Heatmap Overlay")
        gradcam_opacity = st.slider(t["gradcam_opacity"], 0.0, 1.0, 0.5, 0.05)

        contour_overlay = extract_tumor_contours(pacs_img, heatmap, alpha=gradcam_opacity) if heatmap is not None else None
        standard_overlay = overlay_gradcam(pacs_img, heatmap) if heatmap is not None else None

        v_tabs = st.tabs([
            t["tab_gradcam"], t["tab_contours"], "T1-Native",
            "T1-Contrast (Gd)", "T2-Weighted", "FLAIR (Edema)", t["tab_dicom"]
        ])

        with v_tabs[0]:
            if standard_overlay is not None:
                st.image(standard_overlay, caption="Grad-CAM Focus Overlay", use_container_width=True)
            else:
                st.image(pacs_img, caption="Original Scan", use_container_width=True)
        with v_tabs[1]:
            if contour_overlay is not None:
                st.image(contour_overlay, caption="Contours: Red = Core | Cyan = Edema", use_container_width=True)
            else:
                st.image(pacs_img, caption="Original Scan", use_container_width=True)
        with v_tabs[2]:
            st.image(seq_dict["T1-Native"], caption="T1-Weighted Native", use_container_width=True)
        with v_tabs[3]:
            st.image(seq_dict["T1-Contrast (Gd)"], caption="T1 + Gadolinium Contrast", use_container_width=True)
        with v_tabs[4]:
            st.image(seq_dict["T2-Weighted"], caption="T2-Weighted", use_container_width=True)
        with v_tabs[5]:
            st.image(seq_dict["FLAIR (Fluid Attenuated)"], caption="FLAIR Fluid Attenuated", use_container_width=True)
        with v_tabs[6]:
            st.markdown(
                f"""
                <div class="dicom-box">
                <b>[DICOM HEADER TELEMETRY]</b><br>
                - Patient ID: {dicom_info['Patient_Token']}<br>
                - Accession No: {dicom_info['Accession_No']}<br>
                - Scanner: {dicom_info['Manufacturer']}<br>
                - Field Strength: {dicom_info['Magnetic_Field']}<br>
                - Matrix: {dicom_info['Matrix_Size']}<br>
                - Slice Thickness: {dicom_info['Slice_Thickness']}<br>
                - TR/TE: {dicom_info['Repetition_Time_TR']} / {dicom_info['Echo_Time_TE']}<br>
                - PHI Status: {dicom_info['PHI_Status']}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        res_col1, res_col2 = st.columns([1.2, 1])
        with res_col1:
            if conf1 >= threshold:
                card(
                    f"{DATA[label1]['emoji']} {DATA[label1]['title']}",
                    f"Model confidence: {conf1:.1f}%  |  RECIST: {recist_res['recist_category']}",
                    COLORS[label1],
                )
                display_label = label1
            else:
                card(
                    t["uncertain"],
                    f"Prediction ({DATA[label1]['title']}) is below {threshold}% threshold.",
                    "#7f8c8d",
                )
                display_label = label1

            st.markdown(
                f"""
                <div style="background: #353044; border: 1.5px solid #5E5373; border-radius: 12px; padding: 14px; margin-top: 10px; box-shadow: 0 4px 15px rgba(42,37,57,0.35);">
                    <div style="color: #DBD8E3; font-weight: 800; font-size: 13px;">📊 RECIST 1.1 ONCOLOGY VOLUMETRICS</div>
                    <div style="display: flex; justify-content: space-between; margin-top: 6px; font-size: 12.5px; color: #DBD8E3;">
                        <span>{t['est_volume']}: <b>{recist_res['volume_cm3']} cm³</b></span>
                        <span>{t['max_diam']}: <b>{recist_res['max_diameter_mm']} mm</b></span>
                    </div>
                    <div style="font-size: 12px; color: #b8aec9; margin-top: 4px;">
                        {t['mass_effect']}: <b style="color: #ffffff;">{recist_res['mass_effect']}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with res_col2:
            st.plotly_chart(gauge(conf1, COLORS[label1]), key="gauge_pacs", use_container_width=True)

        st.subheader(t["prob_distribution"])
        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(donut(pred), key="donut_pacs", use_container_width=True)
        with g2:
            st.plotly_chart(bars(pred), key="bars_pacs", use_container_width=True)

        st.divider()
        st.subheader(t["dictation_header"])
        st.caption(t["dictation_caption"])

        default_note = (
            f"Lesion in brain parenchyma consistent with {DATA[display_label]['title']}. "
            f"Estimated volume: {recist_res['volume_cm3']} cm3 with {recist_res['mass_effect'].lower()}."
        )
        clinician_notes = st.text_area("Impression Notes", value=default_note, height=85)

        st.divider()
        st.subheader(t["guidelines_header"])
        show_tabs(display_label)

        st.divider()
        st.subheader(t["export_header"])

        down_col1, down_col2 = st.columns(2)
        current_clinician = get_current_user().get("name", "Dr. Sarah Mitchell, MD")

        with down_col1:
            try:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_pdf_path = os.path.join(tmp_dir, "tumor_report.pdf")
                    create_pdf_report(
                        DATA[display_label]['title'], conf1, DATA[display_label]['overview'],
                        filepath=tmp_pdf_path, recist_data=recist_res, dicom_data=dicom_info,
                        clinician_name=current_clinician, dictated_notes=clinician_notes
                    )
                    with open(tmp_pdf_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                    st.download_button(
                        t["download_pdf"],
                        pdf_bytes,
                        file_name=f"NeuroScan_Report_{dicom_info['Accession_No']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                logger.error(f"PDF creation failed: {e}")
                st.warning("PDF report generation encountered an error.")

        with down_col2:
            fhir_json = generate_fhir_diagnostic_report(
                patient_token=dicom_info["Patient_Token"],
                accession_no=dicom_info["Accession_No"],
                predicted_condition=label1,
                confidence=conf1,
                recist_metrics=recist_res,
                clinician_name=current_clinician
            )
            st.download_button(
                t["download_fhir"],
                fhir_json.encode("utf-8"),
                file_name=f"FHIR_DiagnosticReport_{dicom_info['Accession_No']}.json",
                mime="application/json",
                use_container_width=True
            )


# ---------------- PAGE 2: NEUROCOPILOT AI SURGICAL RISK (UNIQUE KILLER FEATURE) ----------------
def neuro_copilot_page():
    st.subheader("🧠 NeuroCopilot™ AI Surgical Resectability & Risk Calculator")
    st.markdown(
        "Advanced clinical decision support: Simulates surgical feasibility, evaluates proximity to eloquent "
        "brain cortex (Broca's / Wernicke's / Motor Strip), predicts functional Karnofsky Performance Status (KPS), "
        "and projects 24-month progression-free survival under multimodality therapies."
    )

    c_param, c_vis = st.columns([1.1, 2])

    with c_param:
        st.markdown("#### ⚙️ Patient & Anatomical Parameters")
        target_condition = st.selectbox(
            "Pathology Under Consideration",
            CLASSES,
            format_func=lambda k: f"{DATA[k]['emoji']} {DATA[k]['title']}"
        )
        tumor_vol = st.slider("Tumor Volume (cm³)", 1.0, 50.0, 18.5, 0.5)

        eloquence = st.selectbox(
            "Eloquent Cortex Proximity",
            [
                "Directly Involves Primary Motor/Speech Cortex",
                "Adjacent (Within 5mm of Eloquent Area)",
                "Non-Eloquent Lobe (Frontal/Temporal Pole)"
            ]
        )

        vascular = st.checkbox("Major Vascular Encasement (ICA / MCA / Sinus)", value=True)
        pt_age = st.slider("Patient Age (Years)", 18, 85, 56)
        pre_kps = st.slider("Pre-Operative KPS Score", 40, 100, 80, 10, help="100 = Normal, 80 = Normal activity with effort, 50 = Requires considerable assistance")

        # Run Surgical Simulation
        risk_res = calculate_surgical_risk(
            tumor_class=target_condition,
            volume_cm3=tumor_vol,
            eloquent_proximity=eloquence,
            vascular_encasement=vascular,
            patient_age=pt_age,
            preop_kps=pre_kps
        )

    with c_vis:
        # Score banner
        pct = risk_res["resectability_pct"]
        score_color = "#10b981" if pct >= 75 else ("#f59e0b" if pct >= 45 else "#ef4444")

        st.markdown(
            f"""
            <div style="background: #353044; border: 2px solid {score_color};
                        border-radius: 14px; padding: 18px 22px; margin-bottom: 16px;
                        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px {score_color}33;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 11px; font-weight: 800; color: #DBD8E3; text-transform: uppercase;">
                            Gross Total Resection (GTR) Feasibility Index
                        </div>
                        <div style="font-size: 26px; font-weight: 900; color: {score_color}; margin-top: 2px;">
                            {pct}% Feasibility
                        </div>
                        <div style="font-size: 13px; font-weight: 700; color: #ffffff; margin-top: 4px;">
                            Strategy: {risk_res['resectability_class']}
                        </div>
                    </div>
                    <div style="text-align: right; border-left: 1px solid rgba(219, 216, 227, 0.2); padding-left: 18px;">
                        <div style="font-size: 11px; font-weight: 800; color: #DBD8E3;">WHO CNS STAGING</div>
                        <div style="font-size: 13.5px; font-weight: 800; color: #ffffff;">{risk_res['who_grade']}</div>
                        <div style="font-size: 11.5px; color: #b8aec9; margin-top: 3px;">Projected Post-Op KPS: <b>{risk_res['projected_postop_kps']}</b></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        r_tab1, r_tab2, r_tab3 = st.tabs(["🎯 Surgical Risk Radar", "📈 24-Month Survival Trajectory", "🧬 Molecular Biomarkers"])
        with r_tab1:
            st.plotly_chart(render_risk_radar(risk_res["risk_scores"]), key="risk_radar", use_container_width=True)
        with r_tab2:
            st.plotly_chart(render_survival_trajectory(target_condition, pct), key="surv_trajectory", use_container_width=True)
        with r_tab3:
            st.markdown("##### 🧬 Recommended Molecular Biomarkers (NCCN Guidelines)")
            st.markdown("Mandatory diagnostic workup for histopathologic precision:")
            for m in risk_res["molecular_markers"]:
                st.markdown(f"- 🧪 **{m}**")
            st.info(f"**Recommended Adjuvant Protocol:** {risk_res['chemo_regimen']}")


# ---------------- PAGE 3: LONGITUDINAL TUMOR BOARD ----------------
def longitudinal_page():
    st.subheader("📈 Longitudinal Patient Journey & Tumor Board Timeline")
    st.markdown("Track tumor volume progression or shrinkage over time across surgical, chemo, and radiotherapy intervals (RECIST 1.1 Criteria).")

    patient_case = st.selectbox(
        "Select Clinical Case Timeline",
        [
            "Case #1: Glioblastoma Post-Resection & Radiotherapy (PX-4821)",
            "Case #2: Meningioma Observation & Stereotactic Radiosurgery (PX-9920)",
            "Case #3: Pituitary Macroadenoma Medical Management (PX-1044)"
        ]
    )

    t_base, t_follow = st.columns(2)

    if "Glioblastoma" in patient_case:
        img1_path = SAMPLES["glioma"]
        img2_path = SAMPLES["notumor"] if os.path.exists(SAMPLES["notumor"]) else SAMPLES["glioma"]
        base_vol, follow_vol = 18.4, 5.2
        base_diam, follow_diam = 34.0, 16.5
    elif "Meningioma" in patient_case:
        img1_path = SAMPLES["meningioma"]
        img2_path = SAMPLES["meningioma"]
        base_vol, follow_vol = 12.8, 11.9
        base_diam, follow_diam = 28.0, 26.8
    else:
        img1_path = SAMPLES["pituitary"]
        img2_path = SAMPLES["pituitary"]
        base_vol, follow_vol = 8.6, 3.8
        base_diam, follow_diam = 22.0, 13.0

    delta_vol = round(((follow_vol - base_vol) / base_vol) * 100, 1)
    delta_diam = round(follow_diam - base_diam, 1)

    with t_base:
        st.markdown("#### 📅 Baseline MRI (Day 0)")
        if os.path.exists(img1_path):
            st.image(Image.open(img1_path), caption="Baseline T1-Gd Scan", use_container_width=True)
        st.metric("Baseline Volume", f"{base_vol} cm³")
        st.metric("Max Diameter", f"{base_diam} mm")

    with t_follow:
        st.markdown("#### 📅 Follow-Up MRI (Day 90)")
        if os.path.exists(img2_path):
            st.image(Image.open(img2_path), caption="90-Day Follow-Up Scan", use_container_width=True)
        st.metric("Follow-Up Volume", f"{follow_vol} cm³", delta=f"{delta_vol}%")
        st.metric("Max Diameter", f"{follow_diam} mm", delta=f"{delta_diam} mm")

    st.divider()
    if delta_vol <= -30.0:
        recist_status = "Partial Response (PR) — Significant Tumor Regression"
        badge_color = "#10b981"
    elif delta_vol >= 20.0:
        recist_status = "Progressive Disease (PD) — Interval Growth Observed"
        badge_color = "#ef4444"
    else:
        recist_status = "Stable Disease (SD) — Controlled Mass Dimensions"
        badge_color = "#f59e0b"

    st.markdown(
        f"""
        <div style="background: rgba(8, 20, 28, 0.95); border: 2px solid {badge_color};
                    border-radius: 12px; padding: 16px; margin: 10px 0;">
            <div style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">
                RECIST 1.1 Treatment Response Classification
            </div>
            <div style="font-size: 18px; font-weight: 800; color: {badge_color}; margin-top: 4px;">
                {recist_status}
            </div>
            <div style="font-size: 13px; color: #cbd5e1; margin-top: 6px;">
                Delta Volume: <b>{delta_vol}%</b> &nbsp;|&nbsp; Delta Diameter: <b>{delta_diam} mm</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("👥 Multi-Disciplinary Tumor Board (MDT) Decision")
    tb1, tb2, tb3 = st.columns(3)
    with tb1:
        card("👨‍⚕️ Neurosurgery", "Surgical cavity stable. No immediate revision required.", "#0ea5e9")
    with tb2:
        card("☢️ Radiation Oncology", "Completed 60 Gy adjuvant radiation. Radiosensitivity confirmed.", "#8b5cf6")
    with tb3:
        card("💊 Medical Oncology", "Maintain current temozolomide chemotherapy cycle.", "#10b981")


# ---------------- PAGE 4: BATCH UPLOAD & TRIAGE ----------------
def batch_page():
    st.subheader("📁 Batch MRI Upload & Clinical Triage")
    st.markdown("Upload multiple MRI studies to batch process predictions, calculate RECIST volumes, and triage urgent cases.")

    uploaded_files = st.file_uploader(
        "Upload multiple MRI scans (DICOM / JPG / PNG)",
        type=["jpg", "jpeg", "png", "dcm"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        model = load_model(MODEL_PATH)
        if model is None:
            return

        results = []
        progress_bar = st.progress(0)

        for i, f in enumerate(uploaded_files):
            try:
                img = Image.open(f)
                valid_img = validate_image(img)
                x = preprocess_image(valid_img)
                pred = predict(model, x)

                idx = int(np.argmax(pred))
                label = CLASSES[idx]
                conf = float(pred[idx]) * 100

                caliper = 22.0 if label != "notumor" else 0.0
                recist = compute_recist_metrics(label, conf, caliper, caliper * 0.75)
                priority = "🔴 URGENT" if (label == "glioma" and conf > 75) else ("🟡 ROUTINE" if label != "notumor" else "🟢 NORMAL")

                res_entry = {
                    "Priority": priority,
                    "Accession": f"ACC-{f.name[:6].upper()}",
                    "Filename": f.name,
                    "AI Diagnosis": DATA[label]["title"],
                    "Confidence (%)": round(conf, 1),
                    "Est. Volume (cm³)": recist["volume_cm3"],
                    "RECIST Category": recist["recist_category"]
                }
                results.append(res_entry)
            except Exception as e:
                results.append({
                    "Priority": "⚠️ ERROR",
                    "Accession": "N/A",
                    "Filename": f.name,
                    "AI Diagnosis": "Processing Error",
                    "Confidence (%)": 0.0,
                    "Est. Volume (cm³)": 0.0,
                    "RECIST Category": str(e)
                })
            progress_bar.progress((i + 1) / len(uploaded_files))

        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Clinical Triage CSV Report", csv, "batch_triage_results.csv", "text/csv")


# ---------------- PAGE 5: COMPARE SCANS ----------------
def compare_page():
    st.subheader("⚖️ Side-by-Side Multi-Scan Comparison")
    st.markdown("Compare two distinct patient MRI scans side-by-side with independent neural inferences.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Patient Study A**")
        f1 = st.file_uploader("Upload first MRI", type=["jpg", "jpeg", "png"], key="cmp1")
    with col2:
        st.markdown("**Patient Study B**")
        f2 = st.file_uploader("Upload second MRI", type=["jpg", "jpeg", "png"], key="cmp2")

    if f1 or f2:
        model = load_model(MODEL_PATH)
        if not model:
            return
        c1, c2 = st.columns(2)
        for idx, (f, c) in enumerate([(f1, c1), (f2, c2)]):
            with c:
                if f:
                    try:
                        img = Image.open(f)
                        valid_img = validate_image(img)
                        x = preprocess_image(valid_img)
                        pred = predict(model, x)

                        top_idx = int(np.argmax(pred))
                        label = CLASSES[top_idx]
                        conf = float(pred[top_idx]) * 100

                        st.image(valid_img, caption=f.name, use_container_width=True)
                        card(
                            f"{DATA[label]['emoji']} {DATA[label]['title']}",
                            f"Confidence: {conf:.1f}%",
                            COLORS[label],
                        )
                        st.plotly_chart(bars(pred), key=f"bar_{idx}", use_container_width=True)
                    except Exception as e:
                        st.error(f"Error processing {f.name}: {e}")
                else:
                    st.info("Upload scan above to view comparative analysis.")


# ---------------- PAGE 6: CONDITION LIBRARY ----------------
def learn_page():
    st.subheader("📚 Clinical Neuro-Oncology Reference Library")
    choice = st.selectbox(
        "Select condition to inspect", CLASSES,
        format_func=lambda k: f"{DATA[k]['emoji']} {DATA[k]['title']}",
    )
    col1, col2 = st.columns([1, 2])
    with col1:
        if os.path.exists(SAMPLES[choice]):
            st.image(
                Image.open(SAMPLES[choice]),
                caption=f"Sample MRI: {DATA[choice]['title']}",
                use_container_width=True,
            )
        else:
            st.info("Sample scan not available.")
    with col2:
        card(f"{DATA[choice]['emoji']} {DATA[choice]['title']}", DATA[choice]["overview"], COLORS[choice])
        st.markdown(f"**Referral Specialist:** {DATA[choice]['specialists']}")
    show_tabs(choice)


# ---------------- PAGE 7: SAFETY & VALIDATION METRICS ----------------
def performance_page():
    st.subheader("📊 FDA SaMD Clinical Safety & Validation Metrics")
    st.markdown("Evaluated on 1,600 held-out multi-institutional test MRI images (Kaggle Brain Tumor Dataset).")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Overall Accuracy", "85.25%")
    m2.metric("Macro F1 Score", "0.848")
    m3.metric("Input Tensor", "160 x 160 x 3")
    m4.metric("Architecture", "MobileNetV2 (Frozen ImageNet)")

    st.markdown("### Per-Class Diagnostic Performance")
    metrics_data = {
        "Condition": ["Glioma", "Meningioma", "No Tumor", "Pituitary"],
        "Precision": [0.942, 0.827, 0.906, 0.770],
        "Recall (Sensitivity)": [0.725, 0.695, 0.993, 0.998],
        "F1 Score": [0.819, 0.755, 0.947, 0.869]
    }
    st.table(metrics_data)

    st.markdown("### Confusion Matrix (Clinical Truth vs. Neural Prediction)")
    cm_data = [
        [290, 56, 26, 28],
        [17, 278, 15, 90],
        [0, 2, 397, 1],
        [1, 0, 0, 399]
    ]

    fig = go.Figure(data=go.Heatmap(
        z=cm_data,
        x=["Glioma", "Meningioma", "No Tumor", "Pituitary"],
        y=["Glioma", "Meningioma", "No Tumor", "Pituitary"],
        colorscale='Teal',
        text=cm_data,
        texttemplate="%{text}",
        hovertemplate="True: %{y}<br>Predicted: %{x}<br>Count: %{text}<extra></extra>"
    ))
    fig.update_layout(
        title="Confusion Matrix Heatmap",
        xaxis_title="Predicted Condition",
        yaxis_title="True Condition",
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(style(fig, 380), key="cm_pacs", use_container_width=True)


# ---------------- PAGE DISPATCHER ----------------
if nav_idx == 0:
    analyze_page()
elif nav_idx == 1:
    neuro_copilot_page()
elif nav_idx == 2:
    longitudinal_page()
elif nav_idx == 3:
    batch_page()
elif nav_idx == 4:
    compare_page()
elif nav_idx == 5:
    learn_page()
else:
    performance_page()
