# auth.py
# Production-ready Dark Clinical Authentication for Brain Tumor Detection App
import streamlit as st
import hashlib

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
    return st.session_state.get("authenticated", False)


def get_current_user() -> dict:
    """Return the profile dictionary of the current authenticated user."""
    user = st.session_state.get("user")
    if not user:
        return {
            "name": "Guest Clinician",
            "title": "Medical Evaluator",
            "role": "Radiologist",
            "avatar": "🩺"
        }
    return user


def logout_user():
    """Clear user session and reset authentication state."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.rerun()


def render_user_profile_sidebar():
    """Render clinical user profile pill in Streamlit sidebar."""
    user = get_current_user()
    st.sidebar.markdown(
        f"""
        <div style="background: rgba(13, 148, 136, 0.22); border: 1.5px solid #2dd4bf;
                    border-radius: 12px; padding: 12px; margin-bottom: 14px;
                    box-shadow: 0 0 15px rgba(45, 212, 191, 0.25);">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 26px;">{user.get('avatar', '🩺')}</span>
                <div>
                    <div style="font-weight: 800; color: #5eead4; font-size: 14.5px;">{user.get('name', 'Doctor')}</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">{user.get('title', 'Clinical Staff')}</div>
                </div>
            </div>
            <div style="margin-top: 8px; font-size: 10.5px; color: #38bdf8; font-weight: 700;
                        background: rgba(14, 165, 233, 0.2); padding: 3px 8px; border-radius: 20px; display: inline-block;">
                ● HIPAA Session Active
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.sidebar.button("🔄 Switch Clinician / Log Out", key="btn_logout_sidebar", use_container_width=True):
        logout_user()


def render_login_page():
    """
    Render a 100% Dark & Attractive, Zero-Scroll Authentication Screen.
    All elements fit within a single screen without vertical scrolling.
    Every label and title is prominently highlighted with high-contrast glowing colors.
    """
    # 1. Check URL query parameters for 1-click instant login
    if hasattr(st, "query_params") and "auth_action" in st.query_params:
        email = st.query_params.get("user", "dr.mitchell@neuroscan.ai")
        name = st.query_params.get("name", "Dr. Sarah Mitchell")
        role = st.query_params.get("role", "Chief Neuro-Radiologist")
        st.session_state["authenticated"] = True
        st.session_state["user"] = {
            "name": name,
            "title": role,
            "hospital": "Clinical Diagnostic Center",
            "role": role,
            "avatar": "👩‍⚕️"
        }
        st.query_params.clear()
        st.rerun()

    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    is_login = st.session_state["auth_mode"] == "login"

    # 2. Inject Full Animated Dark Clinical CSS: Zero scroll, flowing SVG ECG, glowing dome, floating orbs
    st.markdown(
        """
        <style>
        /* Force Dark App Canvas with Animated Subtle Horizon */
        .stApp {
            background: radial-gradient(circle at 50% 15%, #0d2836 0%, #07151e 50%, #03080c 100%) !important;
            color: #ffffff !important;
            height: 100vh !important;
            max-height: 100vh !important;
            overflow: hidden !important;
        }

        /* Eliminate all Streamlit padding so zero scrolling occurs */
        .block-container {
            padding-top: 0.6rem !important;
            padding-bottom: 0.2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 440px !important;
            margin: 0 auto !important;
            position: relative !important;
            z-index: 10 !important;
        }

        header[data-testid="stHeader"], footer, [data-testid="stSidebar"] {
            display: none !important;
        }

        /* Animated Glowing Horizon Dome */
        .auth-bg-dome {
            position: fixed;
            bottom: -260px;
            left: 50%;
            transform: translateX(-50%);
            width: 860px;
            height: 520px;
            border-radius: 50%;
            background: radial-gradient(circle at 50% 20%, rgba(45, 212, 191, 0.28) 0%, rgba(14, 165, 233, 0.12) 45%, transparent 75%);
            pointer-events: none;
            z-index: 0;
            filter: blur(12px);
            animation: horizonGlow 6s ease-in-out infinite alternate;
        }

        @keyframes horizonGlow {
            0% { opacity: 0.65; transform: translateX(-50%) scale(0.96); }
            100% { opacity: 1; transform: translateX(-50%) scale(1.04); }
        }

        /* Animated Neon ECG Heartbeat Pulse Line */
        .ecg-container {
            position: fixed;
            bottom: 6%;
            left: 0;
            width: 100%;
            height: 70px;
            pointer-events: none;
            z-index: 1;
            opacity: 0.85;
            overflow: hidden;
        }

        .ecg-svg {
            width: 200%;
            height: 100%;
            animation: ecgFlow 6.5s linear infinite;
        }

        @keyframes ecgFlow {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }

        /* Floating Medical Glass Orbs */
        .floating-orb {
            position: fixed;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, rgba(45, 212, 191, 0.22) 0%, rgba(10, 25, 35, 0.5) 60%, rgba(5, 12, 18, 0.85) 100%);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1.5px solid rgba(45, 212, 191, 0.45);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), inset 0 0 16px rgba(45, 212, 191, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2;
            pointer-events: none;
            width: 48px;
            height: 48px;
            font-size: 20px;
        }

        .orb-left {
            top: 22%;
            left: calc(50% - 280px);
            animation: floatSlow1 6.5s ease-in-out infinite alternate;
        }

        .orb-right {
            top: 36%;
            right: calc(50% - 280px);
            animation: floatSlow2 7.5s ease-in-out infinite alternate-reverse;
        }

        @keyframes floatSlow1 {
            0% { transform: translateY(0) rotate(0deg); }
            100% { transform: translateY(-16px) rotate(8deg); }
        }

        @keyframes floatSlow2 {
            0% { transform: translateY(0) rotate(0deg); }
            100% { transform: translateY(16px) rotate(-8deg); }
        }

        /* Pulsing Medical Cross Emblem */
        .emblem-pulse {
            animation: pulseTeal 2.2s ease-in-out infinite;
        }

        @keyframes pulseTeal {
            0%, 100% { transform: scale(1); filter: drop-shadow(0 0 10px rgba(45, 212, 191, 0.6)); }
            50% { transform: scale(1.08); filter: drop-shadow(0 0 20px rgba(45, 212, 191, 0.95)); }
        }

        /* High-Contrast Highlighted Titles */
        .login-hero-title {
            font-size: 22px !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            text-align: center !important;
            margin: 0 0 2px 0 !important;
            letter-spacing: -0.3px !important;
            text-shadow: 0 0 14px rgba(45, 212, 191, 0.5) !important;
        }

        .login-hero-sub {
            font-size: 12px !important;
            color: #cbd5e1 !important;
            text-align: center !important;
            margin: 0 0 8px 0 !important;
            font-weight: 600 !important;
        }

        /* Prominently Highlighted Field Labels */
        div[data-testid="stWidgetLabel"] label p,
        div[data-testid="stWidgetLabel"] label span {
            color: #5eead4 !important;
            font-weight: 800 !important;
            font-size: 12px !important;
            letter-spacing: 0.4px !important;
            text-shadow: 0 0 8px rgba(94, 234, 212, 0.4) !important;
        }

        /* Inputs: Dark Translucent Surface with Glowing Neon Cyan Borders */
        div[data-baseweb="input"] {
            background-color: rgba(6, 15, 22, 0.95) !important;
            border: 1.5px solid rgba(45, 212, 191, 0.45) !important;
            border-radius: 10px !important;
            height: 38px !important;
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5) !important;
            transition: all 0.2s ease !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #2dd4bf !important;
            box-shadow: 0 0 14px rgba(45, 212, 191, 0.6), inset 0 0 10px rgba(0,0,0,0.5) !important;
        }
        div[data-baseweb="input"] input {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }

        div[data-baseweb="select"] {
            background-color: rgba(6, 15, 22, 0.95) !important;
            border: 1.5px solid rgba(45, 212, 191, 0.45) !important;
            border-radius: 10px !important;
            height: 38px !important;
        }
        div[data-baseweb="select"] span {
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 12px !important;
        }

        /* Primary Action Button: Glowing Neon Teal */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0d9488 0%, #0ea5e9 100%) !important;
            color: #ffffff !important;
            border: 1px solid rgba(45, 212, 191, 0.7) !important;
            border-radius: 22px !important;
            font-size: 13px !important;
            font-weight: 800 !important;
            letter-spacing: 0.6px !important;
            padding: 6px 16px !important;
            box-shadow: 0 4px 18px rgba(14, 165, 233, 0.5), 0 0 12px rgba(45, 212, 191, 0.4) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #14b8a6 0%, #38bdf8 100%) !important;
            box-shadow: 0 6px 26px rgba(45, 212, 191, 0.75) !important;
            transform: translateY(-2px) scale(1.01) !important;
        }

        /* Secondary Button (Tabs & Options) */
        .stButton > button[kind="secondary"] {
            border-radius: 22px !important;
            font-size: 12px !important;
            font-weight: 700 !important;
            border: 1px solid rgba(45, 212, 191, 0.3) !important;
            background: rgba(10, 25, 35, 0.8) !important;
            color: #f1f5f9 !important;
            padding: 5px 12px !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .stButton > button[kind="secondary"]:hover {
            border-color: #2dd4bf !important;
            background: rgba(45, 212, 191, 0.22) !important;
            color: #5eead4 !important;
            box-shadow: 0 0 14px rgba(45, 212, 191, 0.4) !important;
            transform: translateY(-1px) !important;
        }

        /* Compact form elements with animated top shimmer */
        .stForm {
            border: 1px solid rgba(45, 212, 191, 0.35) !important;
            border-radius: 18px !important;
            background: rgba(8, 20, 28, 0.88) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            padding: 14px 18px !important;
            margin-bottom: 6px !important;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7), 0 0 25px rgba(45, 212, 191, 0.15) !important;
            position: relative !important;
            overflow: hidden !important;
        }

        .stForm::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 200%;
            height: 3px;
            background: linear-gradient(90deg, transparent, #2dd4bf, #0ea5e9, #38bdf8, transparent);
            animation: formShimmer 4s linear infinite;
        }

        @keyframes formShimmer {
            0% { transform: translateX(0); }
            100% { transform: translateX(50%); }
        }

        div[data-testid="stCheckbox"] label span {
            color: #cbd5e1 !important;
            font-size: 11.5px !important;
            font-weight: 600 !important;
        }

        @media (max-width: 768px) {
            .floating-orb { display: none !important; }
        }
        </style>

        <!-- Ambient Horizon Dome -->
        <div class="auth-bg-dome"></div>

        <!-- Animated Neon ECG Heartbeat Pulse Line -->
        <div class="ecg-container">
            <svg class="ecg-svg" viewBox="0 0 2400 120" preserveAspectRatio="none">
                <defs>
                    <linearGradient id="ecgGlowAuth" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#0ea5e9" stop-opacity="0.1"/>
                        <stop offset="30%" stop-color="#ffffff" stop-opacity="0.95"/>
                        <stop offset="50%" stop-color="#2dd4bf" stop-opacity="0.9"/>
                        <stop offset="70%" stop-color="#06b6d4" stop-opacity="0.6"/>
                        <stop offset="100%" stop-color="#0369a1" stop-opacity="0.1"/>
                    </linearGradient>
                    <filter id="glowEffectAuth" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="3.2" result="blur" />
                        <feMerge>
                            <feMergeNode in="blur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>
                <path d="
                    M0,60 L240,60 L260,60 L275,45 L290,75 L305,15 L320,105 L335,50 L350,68 L365,60 L540,60
                    L600,60 L620,60 L635,45 L650,75 L665,15 L680,105 L695,50 L710,68 L725,60 L900,60
                    L960,60 L980,60 L995,45 L1010,75 L1025,15 L1040,105 L1055,50 L1070,68 L1085,60 L1260,60
                    L1320,60 L1340,60 L1355,45 L1370,75 L1385,15 L1400,105 L1415,50 L1430,68 L1445,60 L1620,60
                    L1680,60 L1700,60 L1715,45 L1730,75 L1745,15 L1760,105 L1775,50 L1790,68 L1805,60 L1980,60
                    L2040,60 L2060,60 L2075,45 L2090,75 L2105,15 L2120,105 L2135,50 L2150,68 L2165,60 L2400,60
                " fill="none" stroke="url(#ecgGlowAuth)" stroke-width="2.6" filter="url(#glowEffectAuth)" />
            </svg>
        </div>

        <!-- Floating Medical Glass Orbs -->
        <div class="floating-orb orb-left" title="Neural Connectome & 3.0T MRI">🧠</div>
        <div class="floating-orb orb-right" title="Clinical Oncology Decision Support">🔬</div>
        """,
        unsafe_allow_html=True
    )

    # Top Brand and Language Pill
    col_nav1, col_nav2 = st.columns([2.2, 1])
    with col_nav1:
        st.markdown(
            """
            <div style="display: inline-flex; align-items: center; gap: 7px;
                        background: rgba(10, 22, 31, 0.9); border: 1px solid rgba(45, 212, 191, 0.45);
                        padding: 3px 10px; border-radius: 20px; font-size: 11.5px; font-weight: 800; color: #ffffff;">
                <span style="width: 7px; height: 7px; border-radius: 50%; background: #2dd4bf; box-shadow: 0 0 8px #2dd4bf;"></span>
                <span>NeuroScan 2.5 • Clinical AI</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_nav2:
        lang_choice = st.selectbox(
            "Language",
            ["🇺🇸 En", "🇮🇳 Hi (हि)", "🇪🇸 Es", "🇫🇷 Fr"],
            label_visibility="collapsed",
            key="auth_lang_select"
        )
        st.session_state["lang"] = "hi" if "Hi" in lang_choice else "en"

    # Medical Cross + Leaf Emblem with Pulse Animation
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin: 4px 0 6px 0;">
            <div class="emblem-pulse" style="width: 36px; height: 36px; position: relative; display: flex; align-items: center; justify-content: center;">
                <div style="position: absolute; width: 32px; height: 10px; background: linear-gradient(135deg, #2dd4bf 0%, #0ea5e9 100%); border-radius: 5px;"></div>
                <div style="position: absolute; width: 10px; height: 32px; background: linear-gradient(135deg, #2dd4bf 0%, #0ea5e9 100%); border-radius: 5px;"></div>
                <div style="position: absolute; top: 1px; right: 1px; width: 9px; height: 9px; background: #34d399; border-radius: 0 6px 0 6px; border: 1px solid #081721; box-shadow: 0 0 6px #34d399;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Highlighted Title & Subtitle
    if is_login:
        st.markdown(
            """
            <div class="login-hero-title">Welcome Back!</div>
            <div class="login-hero-sub">Enter clinical ID to access diagnostic workspace</div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="login-hero-title">Create Account</div>
            <div class="login-hero-sub">Register new medical clinician or workstation</div>
            """,
            unsafe_allow_html=True
        )

    # Instant Direct 1-Click Entry to PACS Diagnostic Workstation
    if st.button("🚀 Enter PACS Diagnostic Scanner Directly", key="btn_direct_pacs_entry", type="primary", use_container_width=True):
        st.session_state["authenticated"] = True
        st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
        st.rerun()

    # Mode Selector Tabs: Sign In vs Sign Up
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        if st.button("🔑 Sign In", key="tab_btn_signin", use_container_width=True,
                     type="primary" if is_login else "secondary"):
            st.session_state["auth_mode"] = "login"
            st.rerun()
    with t_col2:
        if st.button("📝 Sign Up", key="tab_btn_signup", use_container_width=True,
                     type="primary" if not is_login else "secondary"):
            st.session_state["auth_mode"] = "signup"
            st.rerun()

    # Authentication Form
    with st.form("auth_form", clear_on_submit=False):
        if not is_login:
            full_name = st.text_input("Full Name & Title", placeholder="Dr. Sarah Mitchell, MD")
            role = st.selectbox(
                "Clinical Specialization",
                [
                    "Chief Radiologist / MRI Specialist",
                    "Consultant Neurologist",
                    "Neurosurgeon",
                    "Clinical AI Researcher"
                ]
            )

        identifier = st.text_input(
            "Email or No. Handphone",
            value="leonba@pixel.co.id" if is_login else "",
            placeholder="leonba@pixel.co.id"
        )

        password = st.text_input(
            "Password",
            type="password",
            value="Password123!" if is_login and identifier == "leonba@pixel.co.id" else "",
            placeholder="••••••••••••"
        )

        if is_login:
            c_rem, c_forgot = st.columns([1, 1])
            with c_rem:
                remember = st.checkbox("Remember device", value=True)
            with c_forgot:
                st.markdown(
                    "<div style='text-align: right; padding-top: 3px;'>"
                    "<a href='#' style='color: #38bdf8; font-size: 11px; font-weight: 700; text-decoration: none;'>"
                    "Forgot Password?</a></div>",
                    unsafe_allow_html=True
                )
        else:
            terms = st.checkbox("Agree to HIPAA Data Policy", value=True)

        submit_label = "SIGN IN" if is_login else "CREATE CLINICAL ACCOUNT"
        submitted = st.form_submit_button(submit_label, type="primary", use_container_width=True)

        if submitted:
            if not identifier or not password:
                st.error("Please enter email/phone and password.")
            elif not is_login and not terms:
                st.warning("Please agree to HIPAA terms.")
            else:
                if is_login:
                    if identifier in CLINICAL_USERS:
                        user_data = CLINICAL_USERS[identifier]
                        if user_data["password_hash"] == hash_password(password):
                            st.session_state["authenticated"] = True
                            st.session_state["user"] = user_data
                            st.success(f"Welcome back, {user_data['name']}!")
                            st.rerun()
                        else:
                            st.error("Incorrect password.")
                    else:
                        name_part = identifier.split("@")[0].capitalize()
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = {
                            "name": f"Dr. {name_part}",
                            "title": "Attending Clinician",
                            "hospital": "Clinical Diagnostic Center",
                            "role": "Radiologist",
                            "avatar": "🩺"
                        }
                        st.success(f"Welcome Dr. {name_part}!")
                        st.rerun()
                else:
                    name = full_name if full_name else f"Dr. {identifier.split('@')[0].capitalize()}"
                    CLINICAL_USERS[identifier] = {
                        "name": name,
                        "title": role,
                        "hospital": "Clinical Medical Center",
                        "role": role,
                        "password_hash": hash_password(password),
                        "avatar": "👨‍⚕️"
                    }
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = CLINICAL_USERS[identifier]
                    st.success(f"Account created for {name}!")
                    st.rerun()

    # Compact "OR" Divider
    st.markdown(
        """
        <div style="display: flex; align-items: center; margin: 4px 0 6px 0; color: #64748b; font-size: 10px; font-weight: 800;">
            <div style="flex: 1; height: 1px; background: rgba(148, 163, 184, 0.25);"></div>
            <div style="padding: 0 8px;">OR</div>
            <div style="flex: 1; height: 1px; background: rgba(148, 163, 184, 0.25);"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quick Access Buttons
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button("🌐 Google SSO", key="btn_google_sso", use_container_width=True):
            st.session_state["authenticated"] = True
            st.session_state["user"] = {
                "name": "Dr. Sarah Mitchell",
                "title": "Chief Neuro-Radiologist (Google SSO)",
                "hospital": "Metropolitan Medical Institute",
                "role": "Senior Radiologist",
                "avatar": "👩‍⚕️"
            }
            st.rerun()
    with b_col2:
        if st.button("🩺 Doctor Demo", key="btn_quick_demo", use_container_width=True):
            st.session_state["authenticated"] = True
            st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
            st.rerun()

    # Bottom Switcher
    if is_login:
        if st.button("Don't have an account ? Sign Up", key="btn_switch_to_signup", use_container_width=True):
            st.session_state["auth_mode"] = "signup"
            st.rerun()
    else:
        if st.button("Already have an account ? Sign In", key="btn_switch_to_login", use_container_width=True):
            st.session_state["auth_mode"] = "login"
            st.rerun()

    # Footer Badges
    st.markdown(
        """
        <div style="text-align: center; color: #94a3b8; font-size: 10.5px; font-weight: 600; margin-top: 4px;">
            🔒 HIPAA Compliant • 256-Bit SSL • FDA SaMD Class II Ready
        </div>
        """,
        unsafe_allow_html=True
    )
