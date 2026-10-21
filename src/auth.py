# auth.py
# Clinical Authentication for Brain Tumor Detection App
# Styled with Ethereal Obsidian & Bioluminescent Iris Editorial Theme ("A Deeper Kind of Precision")
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


def get_iris_hero_base64() -> str:
    """Retrieve base64 data URI of the bioluminescent iris hero image."""
    try:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "iris_hero.jpg")
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
    """Render clinical user profile pill in Streamlit sidebar using Bioluminescent Iris theme."""
    user = get_current_user()
    st.sidebar.markdown(
        textwrap.dedent(f"""
        <div style="background: linear-gradient(145deg, #0B0616 0%, #06030C 100%);
                    border: 1.5px solid rgba(138, 43, 226, 0.4);
                    border-radius: 16px; padding: 14px 16px; margin-bottom: 16px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 16px rgba(0, 210, 255, 0.15);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 44px; height: 44px; border-radius: 50%; background: #030206; border: 1.5px solid #00D2FF;
                            display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 0 12px rgba(0, 210, 255, 0.35);">
                    {user.get('avatar', '🩺')}
                </div>
                <div>
                    <div style="font-family: 'Playfair Display', serif; font-weight: 700; color: #FFFFFF; font-size: 15px; letter-spacing: 0.2px;">{user.get('name', 'Doctor')}</div>
                    <div style="font-size: 11.5px; color: #00D2FF; font-weight: 600;">{user.get('title', 'Clinical Staff')}</div>
                </div>
            </div>
            <div style="margin-top: 10px; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(138, 43, 226, 0.2); padding-top: 8px;">
                <span style="font-size: 10px; color: #00D2FF; font-weight: 700; background: rgba(0, 210, 255, 0.12);
                             padding: 3px 8px; border-radius: 20px; border: 1px solid rgba(0, 210, 255, 0.4);">
                    ● 01 —— Active Session
                </span>
                <span style="font-size: 10px; color: #B3B0C6; font-weight: 600;">{user.get('hospital', 'Diagnostic Center')}</span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
    if st.sidebar.button("🔄 Switch Clinician / Log Out", key="btn_logout_sidebar", use_container_width=True):
        logout_user()


def render_login_page():
    """
    Render modern, high-fashion editorial authentication interface:
    "A Deeper Kind of Precision"
    Visual Identity:
    - Pitch-black obsidian background (#030206)
    - Bioluminescent electric cyan (#00D2FF) and Iris purple (#8A2BE2) glows
    - Editorial serif typography (Playfair Display) with italic ligatures
    - Outline pill buttons ('EXPLORE WORKSTATION ——>')
    - Numbered editorial columns: '01 ——', '02 ——', '03 ——'
    - Ethereal iris artwork and fine astrolabe compass rings
    """
    if "auth_screen" not in st.session_state:
        st.session_state["auth_screen"] = "welcome"

    screen = st.session_state["auth_screen"]
    iris_b64 = get_iris_hero_base64()

    # Global CSS injection for editorial theme
    st.markdown(
        textwrap.dedent("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        /* Pitch Black Obsidian Canvas */
        .stApp {
            background-color: #030206 !important;
            background: radial-gradient(circle at 65% 15%, rgba(138, 43, 226, 0.22) 0%, rgba(0, 210, 255, 0.08) 35%, #030206 75%) !important;
            color: #F8FAFC !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            min-height: 100vh !important;
        }

        /* Hide Streamlit header & sidebar on login screen */
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

        /* Editorial Top Navigation */
        .editorial-nav-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 0 20px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 28px;
        }

        .editorial-nav-menu-icon {
            display: flex;
            flex-direction: column;
            gap: 5px;
            cursor: pointer;
            width: 24px;
        }
        .editorial-nav-menu-icon span {
            display: block;
            height: 2px;
            width: 22px;
            background: #FFFFFF;
            border-radius: 2px;
        }

        .editorial-nav-links {
            display: flex;
            align-items: center;
            gap: 36px;
            list-style: none;
            margin: 0;
            padding: 0;
        }
        .editorial-nav-links a {
            color: #B3B0C6;
            text-decoration: none;
            font-size: 11.5px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            transition: all 0.25s ease;
        }
        .editorial-nav-links a.active,
        .editorial-nav-links a:hover {
            color: #FFFFFF;
            text-shadow: 0 0 10px rgba(0, 210, 255, 0.6);
        }
        .editorial-nav-links a.active::after {
            content: ' •';
            color: #00D2FF;
        }

        .editorial-nav-actions {
            display: flex;
            align-items: center;
            gap: 20px;
            color: #B3B0C6;
            font-size: 16px;
        }

        /* Hero Typography Styling */
        .hero-kicker {
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #8A2BE2;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .hero-kicker::before {
            content: '';
            display: inline-block;
            width: 18px;
            height: 1px;
            background: #8A2BE2;
        }

        .hero-display-title {
            font-family: 'Playfair Display', serif;
            font-size: 68px;
            line-height: 1.02;
            font-weight: 600;
            color: #FFFFFF;
            letter-spacing: -0.5px;
            margin-bottom: 24px;
            position: relative;
        }

        .hero-display-title .word-kind {
            font-style: italic;
            font-weight: 400;
            color: #FFFFFF;
        }
        .hero-display-title .word-of {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: 48px;
            font-weight: 300;
            color: #00D2FF;
            margin-left: 8px;
        }

        .hero-display-title .word-beauty {
            background: linear-gradient(135deg, #9D4EDD 0%, #00D2FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: block;
            font-weight: 700;
            text-shadow: 0 0 35px rgba(138, 43, 226, 0.35);
        }

        /* Celestial Circle & Star Astrolabe Motif */
        .celestial-compass {
            position: absolute;
            top: 40px;
            left: 170px;
            width: 140px;
            height: 140px;
            border: 1px solid rgba(0, 210, 255, 0.25);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }
        .celestial-star {
            position: absolute;
            top: -6px;
            right: 48px;
            color: #00D2FF;
            font-size: 14px;
        }

        .hero-subtitle {
            font-size: 13.5px;
            font-weight: 600;
            letter-spacing: 1.8px;
            line-height: 1.7;
            text-transform: uppercase;
            color: #B3B0C6;
            max-width: 420px;
            margin-bottom: 32px;
        }

        /* Editorial Right Vertical Bar */
        .editorial-vertical-tags {
            display: flex;
            flex-direction: column;
            gap: 24px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #645F7C;
            border-left: 1px solid rgba(255, 255, 255, 0.08);
            padding-left: 16px;
        }
        .editorial-vertical-tags span {
            transition: color 0.2s ease;
        }
        .editorial-vertical-tags span:hover {
            color: #00D2FF;
        }

        /* Numbered Bottom Editorial Cards (01 ——, 02 ——, 03 ——) */
        .editorial-index-card {
            background: rgba(11, 6, 22, 0.65);
            border: 1px solid rgba(138, 43, 226, 0.25);
            border-radius: 14px;
            padding: 16px 18px;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .editorial-index-card:hover {
            border-color: #00D2FF;
            background: rgba(18, 10, 36, 0.9);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 210, 255, 0.25);
        }
        .editorial-index-num {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: 16px;
            color: #8A2BE2;
            margin-right: 8px;
            font-weight: 600;
        }
        .editorial-index-dash {
            color: #645F7C;
            margin-right: 10px;
        }
        .editorial-index-title {
            font-weight: 800;
            font-size: 14px;
            color: #FFFFFF;
            letter-spacing: 0.2px;
        }
        .editorial-index-sub {
            font-size: 11.5px;
            color: #A5A2B8;
            margin-top: 4px;
            line-height: 1.4;
        }

        /* Buttons Styling */
        div[data-testid="stButton"] button[kind="primary"] {
            background: transparent !important;
            border: 1.5px solid #FFFFFF !important;
            color: #FFFFFF !important;
            border-radius: 30px !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            padding: 10px 28px !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.1) !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            border-color: #00D2FF !important;
            color: #030206 !important;
            background: #00D2FF !important;
            box-shadow: 0 0 25px rgba(0, 210, 255, 0.7) !important;
            transform: translateY(-2px) !important;
        }
        div[data-testid="stButton"] button[kind="primary"] p {
            color: inherit !important;
            font-weight: 800 !important;
        }

        div[data-testid="stButton"] button[kind="secondary"],
        div[data-testid="stButton"] button:not([kind="primary"]) {
            background: rgba(11, 6, 22, 0.7) !important;
            border: 1px solid rgba(138, 43, 226, 0.35) !important;
            color: #F8FAFC !important;
            border-radius: 24px !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            transition: all 0.25s ease !important;
        }
        div[data-testid="stButton"] button:not([kind="primary"]):hover {
            border-color: #00D2FF !important;
            color: #00D2FF !important;
            background: rgba(22, 12, 44, 0.95) !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.3) !important;
        }
        div[data-testid="stButton"] button:not([kind="primary"]) p {
            color: inherit !important;
        }

        /* Form Card Container for Login & Sign Up */
        div[data-testid="stForm"] {
            background: linear-gradient(145deg, rgba(14, 8, 28, 0.95) 0%, rgba(6, 3, 12, 0.98) 100%) !important;
            border-radius: 28px !important;
            padding: 34px 28px 28px 28px !important;
            box-shadow: 0 25px 65px rgba(0, 0, 0, 0.9), 0 0 35px rgba(138, 43, 226, 0.25) !important;
            border: 1.5px solid rgba(138, 43, 226, 0.4) !important;
            max-width: 480px !important;
            margin: 0 auto !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"],
        div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        div[data-testid="stTextInput"] input {
            background-color: #06030F !important;
            color: #FFFFFF !important;
            border-radius: 14px !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            border: 1.5px solid rgba(138, 43, 226, 0.3) !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: #00D2FF !important;
            box-shadow: 0 0 0 3px rgba(0, 210, 255, 0.25) !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #06030F !important;
            border: 1.5px solid rgba(138, 43, 226, 0.3) !important;
            border-radius: 14px !important;
            color: #FFFFFF !important;
        }
        </style>
        """),
        unsafe_allow_html=True
    )

    # Top Editorial Navigation Header (Exact matching reference top bar)
    st.markdown(
        textwrap.dedent("""
        <div class="editorial-nav-bar">
            <div class="editorial-nav-menu-icon" title="Editorial Menu">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <ul class="editorial-nav-links">
                <li><a href="#" class="active">HOME</a></li>
                <li><a href="#">WORKSTATION</a></li>
                <li><a href="#">NEURO-AI</a></li>
                <li><a href="#">EXPERIENCE</a></li>
                <li><a href="#">JOURNAL</a></li>
                <li><a href="#">CONTACT</a></li>
            </ul>
            <div class="editorial-nav-actions">
                <span title="Search Workstation" style="cursor: pointer;">🔍</span>
                <span title="Clinical Briefcase" style="cursor: pointer;">💼</span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    # =========================================================================
    # SCREEN 1: EDITORIAL WELCOME SHOWCASE (Matches user reference image)
    # =========================================================================
    if screen == "welcome":
        # Two-column layout: Left = Serif Display Typography; Right = Iris Bioluminescent Art
        col_left, col_right, col_tags = st.columns([1.1, 1.25, 0.2])

        with col_left:
            st.markdown(
                textwrap.dedent("""
                <div style="position: relative; z-index: 1; padding-top: 14px;">
                    <div class="hero-kicker">A STAGE FOR CLINICAL EXCELLENCE</div>
                    <div class="hero-display-title">
                        <div class="celestial-compass"><span class="celestial-star">✦</span></div>
                        A<br>
                        Deeper<br>
                        <span class="word-kind">Kind</span> <span class="word-of">of</span><br>
                        <span class="word-beauty">Precision</span>
                    </div>
                    <div class="hero-subtitle">
                        ADVANCED AI DIAGNOSTICS & VOLUMETRIC NEURO-ONCOLOGY THAT REVEAL MORE THAN WHAT MEETS THE EYE.
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )

            # Editorial Explore & Account Buttons
            btn_col1, btn_col2 = st.columns([1.1, 1.0])
            with btn_col1:
                if st.button("EXPLORE WORKSTATION ⟶", key="btn_hero_explore", type="primary", use_container_width=True):
                    # Instant access into Chief Radiologist workstation session
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                    st.rerun()

            with btn_col2:
                if st.button("CLINICAL LOG IN", key="btn_hero_login", type="secondary", use_container_width=True):
                    st.session_state["auth_screen"] = "login"
                    st.rerun()

        with col_right:
            # Display the breathtaking Iris Artwork with subtle radial blending
            if iris_b64:
                st.markdown(
                    textwrap.dedent(f"""
                    <div style="display: flex; justify-content: center; align-items: center; position: relative;">
                        <div style="position: relative; border-radius: 24px; overflow: hidden;
                                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), 0 0 40px rgba(138, 43, 226, 0.35);
                                    border: 1px solid rgba(0, 210, 255, 0.25);">
                            <img src="{iris_b64}" style="width: 100%; max-height: 440px; object-fit: cover; display: block;" alt="Bioluminescent Iris">
                            <div style="position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, transparent 60%, #030206 100%); pointer-events: none;"></div>
                        </div>
                    </div>
                    """),
                    unsafe_allow_html=True
                )
            else:
                st.image("assets/iris_hero.jpg", use_column_width=True)

        with col_tags:
            # Vertical Editorial Tags on the far right edge matching user image
            st.markdown(
                textwrap.dedent("""
                <div style="padding-top: 60px;">
                    <div class="editorial-vertical-tags">
                        <span>PRECISION</span>
                        <span>NEURO-AI</span>
                        <span>PLACES</span>
                        <span>BEAUTY</span>
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

        # Bottom Editorial Index Row (01 ——, 02 ——, 03 ——)
        st.markdown(
            textwrap.dedent("""
            <div style="font-size: 11px; font-weight: 800; color: #00D2FF; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 12px;">
                ✦ CLINICAL VERIFICATION & PRESET ACCREDITED PROFILES
            </div>
            """),
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                textwrap.dedent("""
                <div class="editorial-index-card">
                    <div>
                        <span class="editorial-index-num">01</span>
                        <span class="editorial-index-dash">——</span>
                        <span class="editorial-index-title">Dr. Sarah Mitchell</span>
                    </div>
                    <div class="editorial-index-sub">
                        Chief Neuro-Radiologist • Metropolitan Neurological Institute
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )
            if st.button("ENTER AS DR. MITCHELL ⟶", key="btn_c1_mitchell", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                st.rerun()

        with c2:
            st.markdown(
                textwrap.dedent("""
                <div class="editorial-index-card">
                    <div>
                        <span class="editorial-index-num">02</span>
                        <span class="editorial-index-dash">——</span>
                        <span class="editorial-index-title">Dr. Rajiv Sharma</span>
                    </div>
                    <div class="editorial-index-sub">
                        Consultant Neurologist • Apex Brain & Spine Center
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )
            if st.button("ENTER AS DR. SHARMA ⟶", key="btn_c2_sharma", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.sharma@neuroscan.ai"]
                st.rerun()

        with c3:
            st.markdown(
                textwrap.dedent("""
                <div class="editorial-index-card">
                    <div>
                        <span class="editorial-index-num">03</span>
                        <span class="editorial-index-dash">——</span>
                        <span class="editorial-index-title">Leon Bastian</span>
                    </div>
                    <div class="editorial-index-sub">
                        Lead Clinical Data Scientist • BioTech Research Labs
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )
            if st.button("ENTER AS SCIENTIST LEON ⟶", key="btn_c3_leon", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["leonba@pixel.co.id"]
                st.rerun()

    # =========================================================================
    # SCREEN 2: CLINICAL LOG IN SCREEN
    # =========================================================================
    elif screen == "login":
        # Back Button to Showcase
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("‹ BACK TO SHOWCASE", key="btn_back_to_welcome_from_login"):
                st.session_state["auth_screen"] = "welcome"
                st.rerun()

        with st.form("form_login", clear_on_submit=False):
            st.markdown(
                textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 22px;">
                    <div style="font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.5px;">
                        Clinical Log In
                    </div>
                    <div style="font-size: 13px; color: #B3B0C6; margin-top: 6px; line-height: 1.5;">
                        Authenticate your medical credentials to access<br>
                        the 3.0T MRI NeuroScan Workstation.
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )

            identifier = st.text_input(
                "Clinical ID / Email",
                value="dr.mitchell@neuroscan.ai",
                placeholder="Enter email or clinical ID"
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
                    "<a href='#' style='color: #00D2FF; font-size: 11.5px; font-weight: 700; text-decoration: none; text-shadow: 0 0 8px rgba(0,210,255,0.4);'>"
                    "Forgot credentials?</a></div>",
                    unsafe_allow_html=True
                )

            submitted = st.form_submit_button("LOG IN TO WORKSTATION ⟶", type="primary", use_container_width=True)

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

        # Divider & Social / PACS SSO
        st.markdown(
            textwrap.dedent("""
            <div style="display: flex; align-items: center; max-width: 480px; margin: 18px auto 14px auto; color: #8A2BE2; font-size: 11.5px; font-weight: 700;">
                <div style="flex: 1; height: 1px; background: rgba(138, 43, 226, 0.3);"></div>
                <div style="padding: 0 12px;">ENTER VIA CLINICAL SSO</div>
                <div style="flex: 1; height: 1px; background: rgba(138, 43, 226, 0.3);"></div>
            </div>
            """),
            unsafe_allow_html=True
        )

        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button("🌐 Google Clinical", key="sso_google", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                st.rerun()
        with s_col2:
            if st.button("🍎 Apple Health", key="sso_apple", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.sharma@neuroscan.ai"]
                st.rerun()
        with s_col3:
            if st.button("🏥 PACS SmartCard", key="sso_pacs", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["leonba@pixel.co.id"]
                st.rerun()

        # Switch to Sign Up
        st.markdown("<div style='margin-top: 16px; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Need credentials? Create Clinical Account", key="btn_goto_signup", use_container_width=True):
            st.session_state["auth_screen"] = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SCREEN 3: CLINICAL SIGN UP / ACCOUNT REGISTRATION
    # =========================================================================
    elif screen == "signup":
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("‹ BACK TO SHOWCASE", key="btn_back_to_welcome_from_signup"):
                st.session_state["auth_screen"] = "welcome"
                st.rerun()

        with st.form("form_signup", clear_on_submit=False):
            st.markdown(
                textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 22px;">
                    <div style="font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.5px;">
                        Register Credentials
                    </div>
                    <div style="font-size: 13px; color: #B3B0C6; margin-top: 6px; line-height: 1.5;">
                        Create a verified clinical seat for institutional<br>
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
        st.markdown("<div style='margin-top: 16px; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Already registered? Log In to Workstation", key="btn_goto_login", use_container_width=True):
            st.session_state["auth_screen"] = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
