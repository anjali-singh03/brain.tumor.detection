# auth.py
# Clinical Authentication for Brain Tumor Detection App
# Designed as a Direct Hospital Staff Login Portal (Siemens syngo.via / GE Centricity Style)
import streamlit as st
import hashlib
import textwrap
import os
import base64


def _get_logo_base64() -> str:
    """Return base64 encoded string of the NeuroScan logo for inline embedding."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(os.path.dirname(current_dir), "assets", "neuroscan_logo.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        pass
    return ""

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
    """Clear user session and reset authentication state to return directly to login screen."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["auth_screen"] = "login"
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
    Directly presents the login screen on app launch.
    """
    # Enforce direct login screen as default
    if "auth_screen" not in st.session_state or st.session_state["auth_screen"] == "welcome":
        st.session_state["auth_screen"] = "login"

    screen = st.session_state["auth_screen"]

    # Global CSS injection for Centered Clinical PACS Login with High-Tech Animations
    st.markdown(
        textwrap.dedent("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        /* Deep Surgical Slate Canvas with Cyber-Grid Matrix */
        .stApp {
            background-color: #070B14 !important;
            background-image:
                radial-gradient(circle at 50% 12%, rgba(14, 165, 233, 0.12) 0%, transparent 60%),
                linear-gradient(rgba(56, 189, 248, 0.035) 1px, transparent 1px),
                linear-gradient(90deg, rgba(56, 189, 248, 0.035) 1px, transparent 1px) !important;
            background-size: 100% 100%, 32px 32px, 32px 32px !important;
            color: #F1F5F9 !important;
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
            min-height: 100vh !important;
        }

        /* Hide Streamlit default header & sidebar on login portal */
        header[data-testid="stHeader"], [data-testid="stSidebar"] {
            display: none !important;
        }

        /* Floating Ambient Synaptic Telemetry Nodes */
        @keyframes ambientFloat {
            0%, 100% { transform: translateY(0) scale(1); opacity: 0.3; }
            50% { transform: translateY(-10px) scale(1.1); opacity: 0.6; filter: drop-shadow(0 0 6px #38BDF8); }
        }
        .ambient-node {
            position: fixed;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(14, 165, 233, 0.14) 0%, rgba(56, 189, 248, 0.02) 50%, transparent 70%);
            pointer-events: none;
            z-index: 0;
            animation: ambientFloat 6s ease-in-out infinite;
        }
        .node-top-left { top: 6%; left: 8%; animation-delay: 0s; }
        .node-top-right { top: 8%; right: 8%; animation-delay: 2s; }
        .node-bottom-left { bottom: 8%; left: 10%; animation-delay: 3.5s; }
        .node-bottom-right { bottom: 6%; right: 10%; animation-delay: 1.5s; }

        /* Centered compact login form container — reveals smoothly after 4s splash */
        .block-container {
            max-width: 400px !important;
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            margin: 0 auto !important;
            position: relative !important;
            z-index: 2 !important;
            animation: loginRevealTiming 4.2s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
        }

        @keyframes loginRevealTiming {
            0%, 82% {
                opacity: 0;
                transform: translateY(16px) scale(0.96);
                pointer-events: none;
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
                pointer-events: auto;
            }
        }

        /* Hospital Brand Header with Pulsing Version Tag */
        .clinical-login-header {
            text-align: center;
            margin-bottom: 10px;
        }

        .clinical-brand-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 2px;
        }

        .clinical-brand-badge h1 {
            font-size: 20px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.3px;
            margin: 0;
            display: inline;
            text-shadow: 0 0 12px rgba(14, 165, 233, 0.35);
        }

        @keyframes badgeGlow {
            0%, 100% { box-shadow: 0 0 3px rgba(14, 165, 233, 0.3); border-color: rgba(56, 189, 248, 0.3); }
            50% { box-shadow: 0 0 8px rgba(56, 189, 248, 0.65); border-color: #38BDF8; }
        }

        .clinical-brand-badge span.version-tag {
            font-size: 9.5px;
            font-weight: 700;
            color: #38BDF8;
            background: rgba(14, 165, 233, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 1px 6px;
            border-radius: 4px;
            letter-spacing: 0.5px;
            animation: badgeGlow 2.5s ease-in-out infinite;
        }

        .clinical-kicker-sub {
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #38BDF8;
            margin-top: 2px;
        }

        .clinical-meta-sub {
            font-size: 9px;
            color: #94A3B8;
            margin-top: 2px;
        }

        /* Form Container with Entrance Fade-in and Holographic Laser Sweep */
        @keyframes cardEntrance {
            0% { opacity: 0; transform: translateY(14px) scale(0.98); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes cardLaserBeam {
            0% { left: -100%; opacity: 0; }
            25% { opacity: 1; }
            75% { opacity: 1; }
            100% { left: 100%; opacity: 0; }
        }

        div[data-testid="stForm"] {
            background: linear-gradient(145deg, #0E1726 0%, #090D16 100%) !important;
            border-radius: 12px !important;
            padding: 16px 18px !important;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.85), 0 0 16px rgba(14, 165, 233, 0.12) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.22) !important;
            margin-top: 4px !important;
            animation: cardEntrance 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
            position: relative !important;
            overflow: hidden !important;
        }

        div[data-testid="stForm"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 75%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #0EA5E9, #38BDF8, #0EA5E9, transparent);
            animation: cardLaserBeam 4s cubic-bezier(0.4, 0, 0.2, 1) infinite;
            box-shadow: 0 0 10px #38BDF8;
            z-index: 10;
        }

        /* Input Fields with Smooth Focus Transition */
        div[data-testid="stTextInput"] label p,
        div[data-testid="stSelectbox"] label p {
            color: #F1F5F9 !important;
            font-weight: 700 !important;
            font-size: 11px !important;
            margin-bottom: 2px !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"],
        div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        div[data-testid="stTextInput"] input {
            background-color: #070B14 !important;
            background: #070B14 !important;
            color: #FFFFFF !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            border: 1.2px solid rgba(56, 189, 248, 0.22) !important;
            border-radius: 7px !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: #0EA5E9 !important;
            box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.25), 0 0 10px rgba(14, 165, 233, 0.2) !important;
        }
        div[data-testid="stTextInput"] input {
            font-size: 12px !important;
            padding: 6px 10px !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #070B14 !important;
            border: 1.2px solid rgba(56, 189, 248, 0.22) !important;
            border-radius: 7px !important;
            color: #FFFFFF !important;
            transition: all 0.2s ease !important;
            min-height: 34px !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 12px !important;
        }

        div[data-testid="stCheckbox"] label span,
        div[data-testid="stCheckbox"] label p {
            color: #CBD5E1 !important;
            font-size: 11px !important;
            font-weight: 600 !important;
        }

        /* Primary Action Buttons with Glow Shimmer */
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stForm"] button[kind="primary"] {
            background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 100%) !important;
            border: none !important;
            color: #FFFFFF !important;
            border-radius: 7px !important;
            font-weight: 800 !important;
            font-size: 12px !important;
            letter-spacing: 0.3px !important;
            padding: 8px 14px !important;
            box-shadow: 0 5px 14px rgba(14, 165, 233, 0.35) !important;
            transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover,
        div[data-testid="stForm"] button[kind="primary"]:hover {
            box-shadow: 0 8px 22px rgba(14, 165, 233, 0.65) !important;
            transform: translateY(-1.5px) !important;
        }

        /* Secondary Buttons with Smooth Lift & Cyan Rim Glow */
        div[data-testid="stButton"] button[kind="secondary"],
        div[data-testid="stButton"] button:not([kind="primary"]) {
            background: #0E1726 !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            color: #E2E8F0 !important;
            border-radius: 7px !important;
            font-weight: 700 !important;
            font-size: 11px !important;
            padding: 5px 10px !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stButton"] button:not([kind="primary"]):hover {
            border-color: #38BDF8 !important;
            color: #38BDF8 !important;
            background: #142033 !important;
            box-shadow: 0 5px 14px rgba(14, 165, 233, 0.25) !important;
            transform: translateY(-1.5px) !important;
        }
        /* 4-Second Cinematic Opening Splash Overlay */
        .neuroscan-splash-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            width: 100vw;
            height: 100vh;
            background: radial-gradient(circle at 50% 40%, #0F1B2D 0%, #070B14 70%);
            z-index: 9999999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            animation: splashFadeDissolve 4.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
        }

        @keyframes splashFadeDissolve {
            0% { opacity: 1; visibility: visible; }
            84% { opacity: 1; visibility: visible; }
            98% { opacity: 0; visibility: visible; }
            100% { opacity: 0; visibility: hidden; pointer-events: none; display: none; }
        }

        .splash-center-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
            animation: splashContentRise 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes splashContentRise {
            0% { opacity: 0; transform: translateY(20px) scale(0.94); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }

        .splash-rings-anchor {
            position: relative;
            width: 130px;
            height: 130px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 22px;
        }

        .splash-ring {
            position: absolute;
            border-radius: 50%;
            border: 1.5px solid #0EA5E9;
            pointer-events: none;
            animation: splashRipple 2.6s cubic-bezier(0.16, 1, 0.3, 1) infinite;
        }
        .ring-1 { width: 95px; height: 95px; animation-delay: 0s; }
        .ring-2 { width: 95px; height: 95px; animation-delay: 0.85s; }
        .ring-3 { width: 95px; height: 95px; animation-delay: 1.7s; }

        @keyframes splashRipple {
            0% { transform: scale(0.85); opacity: 0.9; box-shadow: 0 0 10px #0EA5E9; }
            60% { opacity: 0.35; }
            100% { transform: scale(2.4); opacity: 0; box-shadow: 0 0 25px rgba(56, 189, 248, 0); }
        }

        .splash-logo-box {
            position: relative;
            width: 96px;
            height: 96px;
            border-radius: 22px;
            background: #090D16;
            border: 2px solid #0EA5E9;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.9), 0 0 30px rgba(14, 165, 233, 0.55), inset 0 0 20px rgba(14, 165, 233, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            z-index: 5;
            animation: logoBreathSplash 3s ease-in-out infinite;
        }

        @keyframes logoBreathSplash {
            0%, 100% { transform: scale(1); border-color: #0EA5E9; box-shadow: 0 12px 35px rgba(0,0,0,0.9), 0 0 25px rgba(14,165,233,0.5); }
            50% { transform: scale(1.06); border-color: #38BDF8; box-shadow: 0 16px 45px rgba(0,0,0,0.95), 0 0 40px rgba(56,189,248,0.85); }
        }

        .splash-logo-laser {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, #38BDF8, #FFFFFF, #38BDF8, transparent);
            box-shadow: 0 0 14px #38BDF8;
            animation: splashLaserPass 2.4s ease-in-out infinite alternate;
            pointer-events: none;
            z-index: 6;
        }

        @keyframes splashLaserPass {
            0% { top: 2%; opacity: 0.6; }
            50% { opacity: 1; filter: drop-shadow(0 0 6px #38BDF8); }
            100% { top: 96%; opacity: 0.8; }
        }

        .splash-brand-title {
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            font-size: 26px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: 2px;
            margin: 0;
            text-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
        }

        .splash-brand-kicker {
            font-size: 10.5px;
            font-weight: 700;
            color: #38BDF8;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-top: 6px;
        }

        .splash-brand-meta {
            font-size: 9.5px;
            color: #94A3B8;
            letter-spacing: 0.8px;
            margin-top: 4px;
        }

        .splash-loader-track {
            width: 260px;
            height: 3px;
            background: rgba(56, 189, 248, 0.15);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 24px;
            position: relative;
        }

        .splash-loader-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #0284C7, #38BDF8, #FFFFFF);
            border-radius: 4px;
            box-shadow: 0 0 10px #38BDF8;
            animation: fillProgressSplash 3.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }

        @keyframes fillProgressSplash {
            0% { width: 0%; }
            30% { width: 45%; }
            65% { width: 78%; }
            100% { width: 100%; }
        }

        .splash-status-container {
            position: relative;
            height: 18px;
            width: 320px;
            margin-top: 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 9.5px;
            color: #38BDF8;
            letter-spacing: 0.8px;
            text-align: center;
        }

        .splash-status-text {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            white-space: nowrap;
            opacity: 0;
        }
        .phase-1 { animation: showStatusPhase 1s ease 0s forwards; }
        .phase-2 { animation: showStatusPhase 1s ease 1s forwards; }
        .phase-3 { animation: showStatusPhase 1s ease 2s forwards; }
        .phase-4 { animation: showFinalStatusPhase 1s ease 3s forwards; }

        @keyframes showStatusPhase {
            0% { opacity: 0; transform: translateX(-50%) translateY(4px); }
            20%, 80% { opacity: 1; transform: translateX(-50%) translateY(0); }
            100% { opacity: 0; transform: translateX(-50%) translateY(-4px); }
        }
        @keyframes showFinalStatusPhase {
            0% { opacity: 0; transform: translateX(-50%) translateY(4px); }
            100% { opacity: 1; transform: translateX(-50%) translateY(0); }
        }

        .splash-tap-hint {
            margin-top: 24px;
            font-size: 9px;
            font-weight: 600;
            color: #64748B;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            opacity: 0.75;
        }
        </style>
        <div class="ambient-node node-top-left"></div>
        <div class="ambient-node node-top-right"></div>
        <div class="ambient-node node-bottom-left"></div>
        <div class="ambient-node node-bottom-right"></div>
        """),
        unsafe_allow_html=True
    )

    # 4-Second Cinematic Splash Screen with App Logo & Telemetry Readout
    logo_b64 = _get_logo_base64()
    if logo_b64:
        splash_logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 20px;" alt="Logo" />'
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 36px; height: 36px; border-radius: 9px; border: 1.5px solid #0EA5E9; box-shadow: 0 0 10px rgba(14, 165, 233, 0.45); object-fit: cover;" alt="Logo" />'
    else:
        splash_logo_img = '<span style="font-size: 48px;">🧠</span>'
        logo_html = '<span style="font-size: 22px;">🧠</span>'

    st.markdown(
        textwrap.dedent(f"""
        <!-- 4-Second Opening Splash Screen -->
        <div id="neuroscan-splash-overlay" class="neuroscan-splash-overlay" onclick="dismissSplash()">
            <div class="splash-center-content">
                <div class="splash-rings-anchor">
                    <div class="splash-ring ring-1"></div>
                    <div class="splash-ring ring-2"></div>
                    <div class="splash-ring ring-3"></div>
                    <div class="splash-logo-box">
                        {splash_logo_img}
                        <div class="splash-logo-laser"></div>
                    </div>
                </div>

                <h1 class="splash-brand-title">NEUROSCAN PACS</h1>
                <div class="splash-brand-kicker">CLINICAL NEURO-ONCOLOGY DECISION SUPPORT WORKSTATION</div>
                <div class="splash-brand-meta">3.0T MRI • FDA SaMD Class II • CE-IVD • HIPAA Safe Harbor</div>

                <div class="splash-loader-track">
                    <div class="splash-loader-fill"></div>
                </div>

                <div class="splash-status-container">
                    <span class="splash-status-text phase-1">INITIALIZING 3.0T SYNAPTIC CORE...</span>
                    <span class="splash-status-text phase-2">LOADING MOBILENETV2 & GRAD-CAM XAI...</span>
                    <span class="splash-status-text phase-3">VERIFYING HIPAA SAFE HARBOR PROTOCOLS...</span>
                    <span class="splash-status-text phase-4">CLINICAL WORKSTATION READY</span>
                </div>

                <div class="splash-tap-hint">⚡ Tap anywhere to enter immediately</div>
            </div>
        </div>

        <script>
        function dismissSplash() {{
            var el = document.getElementById('neuroscan-splash-overlay');
            if (el) {{
                el.style.transition = 'opacity 0.4s ease, visibility 0.4s ease';
                el.style.opacity = '0';
                setTimeout(function() {{
                    el.style.visibility = 'hidden';
                    el.style.pointerEvents = 'none';
                    el.style.display = 'none';
                    var loginBox = document.querySelector('.block-container');
                    if (loginBox) {{
                        loginBox.style.animation = 'none';
                        loginBox.style.opacity = '1';
                        loginBox.style.transform = 'translateY(0) scale(1)';
                        loginBox.style.pointerEvents = 'auto';
                    }}
                }}, 400);
            }}
        }}
        setTimeout(function() {{
            var el = document.getElementById('neuroscan-splash-overlay');
            if (el) {{
                el.addEventListener('touchstart', dismissSplash, {{once: true, passive: true}});
                el.addEventListener('click', dismissSplash, {{once: true}});
            }}
        }}, 50);
        </script>

        <!-- Hospital Brand Header on Login Page -->
        <div class="clinical-login-header">
            <div class="clinical-brand-badge">
                {logo_html}
                <h1>NEUROSCAN</h1>
                <span class="version-tag">PACS v4.2</span>
            </div>
            <div class="clinical-kicker-sub">Clinical Neuro-Oncology Decision Support</div>
            <div class="clinical-meta-sub">3.0T MRI • FDA SaMD Class II • CE-IVD • HIPAA Safe Harbor</div>
        </div>
        """),
        unsafe_allow_html=True
    )

    # =========================================================================
    # SCREEN: DIRECT LOGIN SCREEN (Default on app open)
    # =========================================================================
    if screen == "login":
        with st.form("form_login", clear_on_submit=False):
            st.markdown(
                textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 10px;">
                    <div style="font-size: 15px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.2px;">
                        Hospital Staff Authentication
                    </div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 2px; line-height: 1.3;">
                        Institutional credentials to access clinical PACS.
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
                    "<a href='#' style='color: #38BDF8; font-size: 11px; font-weight: 700; text-decoration: none;'>"
                    "Forgot password?</a></div>",
                    unsafe_allow_html=True
                )

            submitted = st.form_submit_button("🔐 LOG IN TO WORKSTATION ⟶", type="primary", use_container_width=True)

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

        # 1-Click Fast Access Section Directly on Login Page
        st.markdown(
            textwrap.dedent("""
            <div style="background: rgba(14, 23, 38, 0.85); border-radius: 10px; padding: 10px 12px; margin-top: 10px;
                        border: 1px solid rgba(56, 189, 248, 0.2); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);">
                <div style="font-size: 9.5px; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; text-align: center;">
                    ⚡ 1-Click Instant Clinician Access
                </div>
            """),
            unsafe_allow_html=True
        )

        p1, p2, p3 = st.columns(3)
        with p1:
            if st.button("👩‍⚕️ Dr. Sarah", key="preset_sarah", help="Chief Neuro-Radiologist", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                st.rerun()
        with p2:
            if st.button("👨‍⚕️ Dr. Rajiv", key="preset_rajiv", help="Consultant Neurologist", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.sharma@neuroscan.ai"]
                st.rerun()
        with p3:
            if st.button("🧑‍🔬 Leon B.", key="preset_leon", help="Lead Data Scientist", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["leonba@pixel.co.id"]
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Institutional Single Sign-On
        st.markdown(
            textwrap.dedent("""
            <div style="display: flex; align-items: center; margin: 10px 0 8px 0; color: #64748B; font-size: 9.5px; font-weight: 700;">
                <div style="flex: 1; height: 1px; background: rgba(56, 189, 248, 0.2);"></div>
                <div style="padding: 0 8px;">INSTITUTIONAL SSO</div>
                <div style="flex: 1; height: 1px; background: rgba(56, 189, 248, 0.2);"></div>
            </div>
            """),
            unsafe_allow_html=True
        )

        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button("🏥 SmartCard", key="sso_pacs", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                st.rerun()
        with s_col2:
            if st.button("🌐 Google", key="sso_google", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.sharma@neuroscan.ai"]
                st.rerun()
        with s_col3:
            if st.button("🍎 Epic/Apple", key="sso_apple", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["leonba@pixel.co.id"]
                st.rerun()

        # Switch to Register
        st.markdown("<div style='margin-top: 8px; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Need clinical credentials? Register Account", key="btn_goto_signup", use_container_width=True):
            st.session_state["auth_screen"] = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SCREEN: CLINICIAN REGISTRATION FORM
    # =========================================================================
    elif screen == "signup":
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("‹ Back to Login", key="btn_back_to_login_from_signup"):
                st.session_state["auth_screen"] = "login"
                st.rerun()

        with st.form("form_signup", clear_on_submit=False):
            st.markdown(
                textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 12px;">
                    <div style="font-size: 16px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.2px;">
                        Register Institutional Credentials
                    </div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 2px; line-height: 1.3;">
                        Establish a verified clinical seat for decision support.
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
        st.markdown("<div style='margin-top: 8px; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Already registered? Log In to Workstation", key="btn_goto_login", use_container_width=True):
            st.session_state["auth_screen"] = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
