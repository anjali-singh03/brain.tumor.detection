# auth.py
# Clinical Authentication for Brain Tumor Detection App
# Designed as a Professional Medical Enterprise PACS Application (Siemens syngo.via / GE Centricity Style)
import streamlit as st
import hashlib
import textwrap
import base64
import os

# Pre-registered clinical user directory
CLINICAL_USERS = {
    "dr.mitchell@neuroscan.ai": {
        "name": "Dr. Sarah Mitchell",
        "title": "Chief Neuro-Radiologist",
        "hospital": "Metropolitan Neurological Institute",
        "role": "Senior Radiologist",
        "password_hash": hashlib.sha256("DemoMedical2026!".encode()).hexdigest(),
        "avatar": "👩‍⚕️"
    },
    "dr.sharma@neuroscan.ai": {
        "name": "Dr. Rajiv Sharma",
        "title": "Consultant Neurologist",
        "hospital": "Apex Brain & Spine Center",
        "role": "Consultant Neurologist",
        "password_hash": hashlib.sha256("Doctor2026!".encode()).hexdigest(),
        "avatar": "👨‍⚕️"
    },
    "leonba@pixel.co.id": {
        "name": "Leon Bastian",
        "title": "Lead Clinical Data Scientist",
        "hospital": "BioTech Research Labs",
        "role": "AI Researcher",
        "password_hash": hashlib.sha256("Password123!".encode()).hexdigest(),
        "avatar": "🧑‍🔬"
    }
}


def get_mri_preview_base64() -> str:
    """Retrieve base64 data URI of the clinical MRI sample scan for PACS preview HUD."""
    try:
        root_dir = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root_dir, "glioma.jpg")
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{data}"
    except Exception:
        pass
    return ""


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 for secure verification."""
    return hashlib.sha256(password.encode()).hexdigest()


def is_authenticated() -> bool:
    """Check if the current session has an authenticated medical user."""
    return bool(st.session_state.get("authenticated", False))


def get_current_user() -> dict:
    """Return the profile dictionary of the current authenticated user."""
    user = st.session_state.get("user")
    if not user:
        return {
            "name": "Guest Clinician",
            "title": "Medical Evaluator",
            "hospital": "Clinical Diagnostic Center",
            "role": "Radiologist",
            "avatar": "🩺"
        }
    return user


def logout_user():
    """Clear user session and reset authentication state to return to login screen."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["auth_screen"] = "welcome"
    st.rerun()


def render_user_profile_sidebar():
    """Render clinical user profile pill in Streamlit sidebar using Clean Medical PACS theme."""
    user = get_current_user()
    st.sidebar.markdown(
        textwrap.dedent(f"""
        <div style="background: linear-gradient(145deg, #0E1726 0%, #090D16 100%);
                    border: 1.5px solid rgba(56, 189, 248, 0.25);
                    border-radius: 12px; padding: 14px 16px; margin-bottom: 16px;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7), 0 0 12px rgba(14, 165, 233, 0.12);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: #090D16; border: 1.5px solid #0EA5E9;
                            display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 0 10px rgba(14, 165, 233, 0.25);">
                    {user.get('avatar', '🩺')}
                </div>
                <div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; color: #FFFFFF; font-size: 14.5px; letter-spacing: -0.1px;">{user.get('name', 'Doctor')}</div>
                    <div style="font-size: 11.5px; color: #38BDF8; font-weight: 600;">{user.get('title', 'Clinical Staff')}</div>
                </div>
            </div>
            <div style="margin-top: 10px; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(56, 189, 248, 0.15); padding-top: 8px;">
                <span style="font-size: 10px; color: #10B981; font-weight: 700; background: rgba(16, 185, 129, 0.12);
                             padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.3);">
                    ● HIPAA Session Active
                </span>
                <span style="font-size: 10px; color: #94A3B8; font-weight: 600;">{user.get('hospital', 'Diagnostic Center')}</span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
    if st.sidebar.button("🔄 Switch Clinician / Log Out", key="btn_logout_sidebar", use_container_width=True):
        logout_user()


def render_login_page():
    """
    Render modern, authentic Clinical PACS Application authentication portal.
    Features:
    - Deep surgical charcoal canvas (#090D16) with clinical cyan accents (#0EA5E9, #38BDF8)
    - 100% interactive, clickable top navigation controls
    - Authentic PACS DICOM 3.0 axial scan HUD preview with calibration grid & telemetry
    - Instant 1-click clinical persona access & institutional credential authentication
    """
    if "auth_screen" not in st.session_state:
        st.session_state["auth_screen"] = "welcome"

    screen = st.session_state["auth_screen"]
    mri_b64 = get_mri_preview_base64()

    # Global CSS injection for Clinical PACS Theme
    st.markdown(
        textwrap.dedent("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        /* Deep Surgical Slate Canvas */
        .stApp {
            background-color: #090D16 !important;
            background: #090D16 !important;
            color: #F1F5F9 !important;
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
            min-height: 100vh !important;
        }

        /* Hide Streamlit default header & sidebar on login portal */
        header[data-testid="stHeader"], [data-testid="stSidebar"] {
            display: none !important;
        }

        .block-container {
            max-width: 1320px !important;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            margin: 0 auto !important;
        }

        /* Interactive Clinical Top Bar */
        .clinical-top-bar {
            background: linear-gradient(135deg, #0E1726 0%, #090D16 100%);
            border: 1.5px solid rgba(56, 189, 248, 0.22);
            border-radius: 12px;
            padding: 12px 18px;
            margin-bottom: 22px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        }

        .clinical-brand-title {
            font-size: 20px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.3px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .clinical-brand-title span {
            font-size: 11px;
            font-weight: 700;
            color: #38BDF8;
            background: rgba(14, 165, 233, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 2px 7px;
            border-radius: 4px;
            letter-spacing: 0.5px;
        }

        /* Clinical Kicker & Headlines */
        .clinical-kicker {
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: #38BDF8;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .clinical-kicker::before {
            content: '';
            display: inline-block;
            width: 14px;
            height: 2px;
            background: #0EA5E9;
        }

        .clinical-display-title {
            font-size: 38px;
            line-height: 1.15;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.5px;
            margin-bottom: 16px;
        }
        .clinical-display-title span {
            color: #38BDF8;
        }

        .clinical-subtitle {
            font-size: 13.5px;
            font-weight: 500;
            line-height: 1.6;
            color: #94A3B8;
            max-width: 500px;
            margin-bottom: 22px;
        }

        /* Regulatory & Standards Badges */
        .clinical-badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 24px;
        }
        .clinical-badge-pill {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.22);
            color: #E2E8F0;
            padding: 5px 11px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }
        .clinical-badge-pill.active {
            background: rgba(14, 165, 233, 0.15);
            border-color: #0EA5E9;
            color: #38BDF8;
        }

        /* Clinical Persona Card */
        .clinical-persona-card {
            background: #0E1726;
            border: 1.5px solid rgba(56, 189, 248, 0.18);
            border-radius: 10px;
            padding: 14px 16px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
        }
        .clinical-persona-card:hover {
            border-color: #0EA5E9;
            background: #142033;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(14, 165, 233, 0.2);
        }
        .clinical-persona-num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            color: #38BDF8;
            margin-right: 6px;
        }
        .clinical-persona-name {
            font-weight: 800;
            font-size: 14px;
            color: #FFFFFF;
        }
        .clinical-persona-sub {
            font-size: 11px;
            color: #94A3B8;
            margin-top: 4px;
            line-height: 1.4;
        }

        /* PACS Scan HUD Container */
        .pacs-hud-frame {
            background: #050811;
            border: 2px solid rgba(56, 189, 248, 0.35);
            border-radius: 12px;
            overflow: hidden;
            position: relative;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.9), 0 0 20px rgba(14, 165, 233, 0.15);
        }

        .pacs-hud-header {
            background: #0B1120;
            border-bottom: 1px solid rgba(56, 189, 248, 0.2);
            padding: 8px 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #38BDF8;
            font-weight: 700;
        }

        .pacs-overlay-corner {
            position: absolute;
            font-family: 'JetBrains Mono', monospace;
            font-size: 10.5px;
            color: #38BDF8;
            line-height: 1.4;
            pointer-events: none;
            z-index: 5;
            background: rgba(5, 8, 17, 0.75);
            padding: 4px 8px;
            border-radius: 4px;
        }
        .pacs-corner-tl { top: 40px; left: 10px; }
        .pacs-corner-tr { top: 40px; right: 10px; text-align: right; }
        .pacs-corner-bl { bottom: 10px; left: 10px; }
        .pacs-corner-br { bottom: 10px; right: 10px; text-align: right; }

        .pacs-hud-telemetry-strip {
            background: #0B1120;
            border-top: 1px solid rgba(56, 189, 248, 0.2);
            padding: 10px 14px;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 10.5px;
            color: #94A3B8;
        }

        /* Buttons Styling */
        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 100%) !important;
            border: none !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            letter-spacing: 0.4px !important;
            padding: 10px 20px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 6px 18px rgba(14, 165, 233, 0.35) !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            box-shadow: 0 8px 24px rgba(14, 165, 233, 0.6) !important;
            transform: translateY(-1.5px) !important;
        }

        div[data-testid="stButton"] button[kind="secondary"],
        div[data-testid="stButton"] button:not([kind="primary"]) {
            background: #0E1726 !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            color: #E2E8F0 !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            font-size: 12.5px !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stButton"] button:not([kind="primary"]):hover {
            border-color: #38BDF8 !important;
            color: #38BDF8 !important;
            background: #142033 !important;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.2) !important;
        }

        /* Form Container for Login & Sign Up */
        div[data-testid="stForm"] {
            background: linear-gradient(145deg, #0E1726 0%, #090D16 100%) !important;
            border-radius: 14px !important;
            padding: 30px 26px !important;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85), 0 0 20px rgba(14, 165, 233, 0.15) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.25) !important;
            max-width: 480px !important;
            margin: 0 auto !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"],
        div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        div[data-testid="stTextInput"] input {
            background-color: #070B14 !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            border: 1.5px solid rgba(56, 189, 248, 0.25) !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: #0EA5E9 !important;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.25) !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #070B14 !important;
            border: 1.5px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
        }
        </style>
        """),
        unsafe_allow_html=True
    )

    # 100% Clickable Interactive Top Header Navigation Bar
    st.markdown("<div class='clinical-top-bar'>", unsafe_allow_html=True)
    c_brand, c_nav1, c_nav2, c_nav3, c_nav4 = st.columns([2.0, 1.1, 1.1, 1.1, 1.1])
    with c_brand:
        st.markdown(
            '<div class="clinical-brand-title">🧠 NEUROSCAN <span>PACS v4.2</span></div>',
            unsafe_allow_html=True
        )
    with c_nav1:
        if st.button("🏥 Diagnostic Portal", key="top_nav_portal", use_container_width=True):
            st.session_state["auth_screen"] = "welcome"
            st.rerun()
    with c_nav2:
        if st.button("🔐 Clinician Login", key="top_nav_login", use_container_width=True):
            st.session_state["auth_screen"] = "login"
            st.rerun()
    with c_nav3:
        if st.button("📝 Register Account", key="top_nav_signup", use_container_width=True):
            st.session_state["auth_screen"] = "signup"
            st.rerun()
    with c_nav4:
        if st.button("⚡ Instant Access", key="top_nav_instant", type="primary", use_container_width=True):
            st.session_state["authenticated"] = True
            st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SCREEN 1: CLINICAL PACS DIAGNOSTIC PORTAL (Clean Medical App)
    # =========================================================================
    if screen == "welcome":
        col_left, col_right = st.columns([1.15, 1.1])

        with col_left:
            st.markdown(
                textwrap.dedent("""
                <div class="clinical-kicker">● METROPOLITAN NEURO-ONCOLOGY INSTITUTE • ENTERPRISE PACS</div>
                <div class="clinical-display-title">
                    Clinical Brain Tumor<br>
                    <span>Decision Support Workstation</span>
                </div>
                <div class="clinical-subtitle">
                    Automated multi-class intracranial lesion detection with MobileNetV2 + Grad-CAM XAI,
                    RECIST 1.1 axial caliper staging, and volumetric neuro-oncology triage.
                </div>
                <div class="clinical-badge-row">
                    <span class="clinical-badge-pill active">● 3.0T MRI Calibrated</span>
                    <span class="clinical-badge-pill">● FDA SaMD Class II</span>
                    <span class="clinical-badge-pill">● HL7 / FHIR R4</span>
                    <span class="clinical-badge-pill">● HIPAA Safe Harbor</span>
                </div>
                """),
                unsafe_allow_html=True
            )

            # Prominent Action Buttons
            btn_col1, btn_col2 = st.columns([1.3, 1.0])
            with btn_col1:
                if st.button("🚀 OPEN CLINICAL WORKSTATION ⟶", key="btn_portal_launch", type="primary", use_container_width=True):
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                    st.rerun()

            with btn_col2:
                if st.button("🔐 STAFF LOG IN", key="btn_portal_login", type="secondary", use_container_width=True):
                    st.session_state["auth_screen"] = "login"
                    st.rerun()

            st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

            # 1-Click Fast Clinician Personas
            st.markdown(
                textwrap.dedent("""
                <div style="font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 10px;">
                    ✦ CLINICAL VERIFICATION & PRESET ACCREDITED PROFILES
                </div>
                """),
                unsafe_allow_html=True
            )

            p1, p2, p3 = st.columns(3)
            with p1:
                st.markdown(
                    textwrap.dedent("""
                    <div class="clinical-persona-card">
                        <div>
                            <span class="clinical-persona-num">01</span>
                            <span class="clinical-persona-name">Dr. Mitchell</span>
                        </div>
                        <div class="clinical-persona-sub">Chief Neuro-Radiology</div>
                    </div>
                    """),
                    unsafe_allow_html=True
                )
                if st.button("ENTER AS DR. MITCHELL ⟶", key="btn_p1_mitchell", use_container_width=True):
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                    st.rerun()

            with p2:
                st.markdown(
                    textwrap.dedent("""
                    <div class="clinical-persona-card">
                        <div>
                            <span class="clinical-persona-num">02</span>
                            <span class="clinical-persona-name">Dr. Sharma</span>
                        </div>
                        <div class="clinical-persona-sub">Consultant Neurologist</div>
                    </div>
                    """),
                    unsafe_allow_html=True
                )
                if st.button("ENTER AS DR. SHARMA ⟶", key="btn_p2_sharma", use_container_width=True):
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = CLINICAL_USERS["dr.sharma@neuroscan.ai"]
                    st.rerun()

            with p3:
                st.markdown(
                    textwrap.dedent("""
                    <div class="clinical-persona-card">
                        <div>
                            <span class="clinical-persona-num">03</span>
                            <span class="clinical-persona-name">Leon Bastian</span>
                        </div>
                        <div class="clinical-persona-sub">Lead AI Scientist</div>
                    </div>
                    """),
                    unsafe_allow_html=True
                )
                if st.button("ENTER AS SCIENTIST LEON ⟶", key="btn_p3_leon", use_container_width=True):
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = CLINICAL_USERS["leonba@pixel.co.id"]
                    st.rerun()

        # Right Column: High-Precision PACS DICOM 3.0 Telemetry & MRI Scan HUD
        with col_right:
            if mri_b64:
                st.markdown(
                    textwrap.dedent(f"""
                    <div class="pacs-hud-frame">
                        <div class="pacs-hud-header">
                            <div>● SIEMENS MAGNETOM SKYRA 3.0T</div>
                            <div>ACQ: 3D MPRAGE</div>
                            <div>STATUS: ONLINE</div>
                        </div>
                        <div style="position: relative; display: flex; justify-content: center; align-items: center; background: #000000;">
                            <img src="{mri_b64}" style="width: 100%; max-height: 380px; object-fit: contain; display: block;" alt="Axial MRI Scan">
                            <!-- Overlay DICOM Tags -->
                            <div class="pacs-overlay-corner pacs-corner-tl">
                                PATIENT: ANON-PX-770405<br>
                                DOB: 1974-06-12<br>
                                GENDER: F
                            </div>
                            <div class="pacs-overlay-corner pacs-corner-tr">
                                MODALITY: 3.0T MRI<br>
                                TE: 2.4 ms / TR: 1900 ms<br>
                                FOV: 240 × 240 mm
                            </div>
                            <div class="pacs-overlay-corner pacs-corner-bl">
                                SERIES: AXIAL T1-Gd<br>
                                SLICE: 88 / 176<br>
                                RECIST: 24.5 mm
                            </div>
                            <div class="pacs-overlay-corner pacs-corner-br">
                                AI: GLIOMA POSITIVE<br>
                                CONFIDENCE: 98.6%<br>
                                VOL: 24.5 cm³
                            </div>
                        </div>
                        <div class="pacs-hud-telemetry-strip">
                            <div><span style="color: #38BDF8; font-weight: 700;">VOXEL:</span> 0.8×0.8×1.0 mm³</div>
                            <div><span style="color: #38BDF8; font-weight: 700;">RECON:</span> Deep Resolve AI</div>
                            <div><span style="color: #10B981; font-weight: 700;">● TRIAGE:</span> URGENT 24H</div>
                            <div><span style="color: #38BDF8; font-weight: 700;">LATENCY:</span> 84 ms</div>
                        </div>
                    </div>
                    """),
                    unsafe_allow_html=True
                )
            else:
                st.image("glioma.jpg", caption="Axial 3.0T MRI Scan HUD", use_column_width=True)

    # =========================================================================
    # SCREEN 2: CLINICIAN LOGIN FORM (Hospital Credentials)
    # =========================================================================
    elif screen == "login":
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("‹ Back to Portal", key="btn_back_to_welcome_from_login"):
                st.session_state["auth_screen"] = "welcome"
                st.rerun()

        with st.form("form_login", clear_on_submit=False):
            st.markdown(
                textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 24px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.3px;">
                        Hospital Staff Authentication
                    </div>
                    <div style="font-size: 12.5px; color: #94A3B8; margin-top: 4px; line-height: 1.5;">
                        Enter your institutional clinical ID to access the<br>
                        3.0T MRI NeuroScan PACS Workstation.
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )

            identifier = st.text_input(
                "Clinical ID / Institutional Email",
                value="dr.mitchell@neuroscan.ai",
                placeholder="Enter email or hospital ID"
            )
            password = st.text_input(
                "Password",
                type="password",
                value="DemoMedical2026!",
                placeholder="Password"
            )

            col_rem, col_forgot = st.columns([1, 1])
            with col_rem:
                st.checkbox("Remember session", value=True)
            with col_forgot:
                st.markdown(
                    "<div style='text-align: right; padding-top: 4px;'>"
                    "<a href='#' style='color: #38BDF8; font-size: 11.5px; font-weight: 700; text-decoration: none;'>"
                    "Forgot password?</a></div>",
                    unsafe_allow_html=True
                )

            submitted = st.form_submit_button("AUTHENTICATE & ENTER WORKSTATION ⟶", type="primary", use_container_width=True)

            if submitted:
                if not identifier or not password:
                    st.error("Please enter email and password.")
                else:
                    if identifier in CLINICAL_USERS:
                        user_entry = CLINICAL_USERS[identifier]
                        if user_entry["password_hash"] == hash_password(password):
                            st.session_state["authenticated"] = True
                            st.session_state["user"] = user_entry
                            st.rerun()
                        else:
                            st.error("Incorrect password. Please try again.")
                    else:
                        name_str = identifier.split("@")[0].replace(".", " ").title()
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = {
                            "name": f"Dr. {name_str}",
                            "title": "Attending Radiologist",
                            "hospital": "Metropolitan Medical Institute",
                            "role": "Radiologist",
                            "avatar": "🩺"
                        }
                        st.rerun()

        # Clinical SSO
        st.markdown(
            textwrap.dedent("""
            <div style="display: flex; align-items: center; max-width: 480px; margin: 18px auto 14px auto; color: #64748B; font-size: 11.5px; font-weight: 700;">
                <div style="flex: 1; height: 1px; background: rgba(56, 189, 248, 0.2);"></div>
                <div style="padding: 0 12px;">ENTER VIA INSTITUTIONAL SSO</div>
                <div style="flex: 1; height: 1px; background: rgba(56, 189, 248, 0.2);"></div>
            </div>
            """),
            unsafe_allow_html=True
        )

        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button("🏥 PACS SmartCard", key="sso_pacs", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                st.rerun()
        with s_col2:
            if st.button("🌐 Google Health", key="sso_google", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.sharma@neuroscan.ai"]
                st.rerun()
        with s_col3:
            if st.button("🍎 Epic / Apple Health", key="sso_apple", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["leonba@pixel.co.id"]
                st.rerun()

        # Switch to Sign Up
        st.markdown("<div style='margin-top: 14px; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Need credentials? Register Clinical Account", key="btn_goto_signup", use_container_width=True):
            st.session_state["auth_screen"] = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SCREEN 3: CLINICIAN REGISTRATION FORM
    # =========================================================================
    elif screen == "signup":
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("‹ Back to Portal", key="btn_back_to_welcome_from_signup"):
                st.session_state["auth_screen"] = "welcome"
                st.rerun()

        with st.form("form_signup", clear_on_submit=False):
            st.markdown(
                textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 24px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.3px;">
                        Register Institutional Credentials
                    </div>
                    <div style="font-size: 12.5px; color: #94A3B8; margin-top: 4px; line-height: 1.5;">
                        Establish a verified clinical seat for institutional<br>
                        FDA SaMD Class II diagnostic analysis.
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )

            full_name = st.text_input("Full Name", placeholder="e.g. Dr. Emily Vance")
            email = st.text_input("Institutional Email", placeholder="e.g. dr.vance@hospital.org")
            password = st.text_input("Password", type="password", placeholder="Enter secure passphrase")
            specialty = st.selectbox(
                "Clinical Department",
                ["Neuro-Radiology", "Neurosurgery", "Clinical Neurology", "Medical Physics & AI"]
            )
            terms = st.checkbox("I agree to HIPAA Safe Harbor and clinical AI protocol terms", value=True)

            submitted = st.form_submit_button("REGISTER & ENTER WORKSTATION ⟶", type="primary", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("Please enter email and password.")
                elif not terms:
                    st.warning("Please agree to HIPAA terms.")
                else:
                    name_final = full_name.strip() if full_name.strip() else f"Dr. {email.split('@')[0].capitalize()}"
                    CLINICAL_USERS[email] = {
                        "name": name_final,
                        "title": f"Specialist, {specialty}",
                        "hospital": "Metropolitan Medical Institute",
                        "role": specialty,
                        "password_hash": hash_password(password),
                        "avatar": "👩‍⚕️"
                    }
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = CLINICAL_USERS[email]
                    st.rerun()

        # Switch to Log In
        st.markdown("<div style='margin-top: 14px; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Already registered? Log In to Workstation", key="btn_goto_login", use_container_width=True):
            st.session_state["auth_screen"] = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
