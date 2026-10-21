# auth.py
# Clinical Authentication for Brain Tumor Detection App
# Styled with iridescent pastel login cards (matching user Image 2) and dark palette sidebar (#2A2539, #353044, #5E5373, #DBD8E3)
import streamlit as st
import hashlib
import textwrap

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
    """Clear user session and reset authentication state to return to login screen."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["auth_screen"] = "welcome"
    st.rerun()


def render_user_profile_sidebar():
    """Render clinical user profile pill in Streamlit sidebar using Deep Dark Purple & Cyan theme."""
    user = get_current_user()
    st.sidebar.markdown(
        textwrap.dedent(f"""
        <div style="background: #160F2E; border: 1.5px solid rgba(168, 85, 247, 0.35);
                    border-radius: 14px; padding: 14px; margin-bottom: 16px;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6), 0 0 14px rgba(168, 85, 247, 0.2);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 44px; height: 44px; border-radius: 50%; background: #0B0616; border: 1.5px solid #00F5D4;
                            display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 0 10px rgba(0, 245, 212, 0.3);">
                    {user.get('avatar', '🩺')}
                </div>
                <div>
                    <div style="font-weight: 800; color: #FFFFFF; font-size: 14.5px; letter-spacing: -0.2px;">{user.get('name', 'Doctor')}</div>
                    <div style="font-size: 11.5px; color: #A5B4FC; font-weight: 500;">{user.get('title', 'Clinical Staff')}</div>
                </div>
            </div>
            <div style="margin-top: 10px; display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 10px; color: #00F5D4; font-weight: 700; background: rgba(168, 85, 247, 0.25);
                             padding: 3px 9px; border-radius: 20px; border: 1px solid #00F5D4;">
                    ● HIPAA Session Active
                </span>
                <span style="font-size: 10px; color: #CBD5E1; font-weight: 600;">{user.get('hospital', 'Diagnostic Center')}</span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
    if st.sidebar.button("🔄 Switch Clinician / Log Out", key="btn_logout_sidebar", use_container_width=True):
        logout_user()


def render_login_page():
    """
    Render modern, elegant authentication interface in Deep Dark Purple with Electric Cyan accents.
    Features:
    - Deep obsidian purple canvas with luminous amethyst & electric cyan ambient glows
    - Mobile-inspired rising glassmorphic rounded cards
    - 3 view modes: 'welcome' (middle screen), 'login' (left screen), 'signup' (right screen)
    - 1-click clinical login presets for instant evaluation
    """
    if "auth_screen" not in st.session_state:
        st.session_state["auth_screen"] = "welcome"

    screen = st.session_state["auth_screen"]

    # Global CSS injection for the login page
    st.markdown(
        textwrap.dedent("""
        <style>
        /* Deep Obsidian Purple Canvas */
        .stApp {
            background-color: #0B0616 !important;
            background: radial-gradient(circle at 50% 12%, #1C0F38 0%, #0D071E 50%, #05020B 100%) !important;
            color: #F8FAFC !important;
            min-height: 100vh !important;
        }

        /* Hide Streamlit header & sidebar on login screen */
        header[data-testid="stHeader"], [data-testid="stSidebar"] {
            display: none !important;
        }

        .block-container {
            max-width: 440px !important;
            padding-top: 1.2rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            margin: 0 auto !important;
        }

        /* Ambient floating glowing bubbles */
        .ambient-bubble-1 {
            position: fixed;
            top: 5%;
            left: 10%;
            width: 280px;
            height: 280px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.4) 0%, rgba(121, 40, 202, 0.1) 70%, transparent 100%);
            filter: blur(40px);
            z-index: 0;
            pointer-events: none;
        }
        .ambient-bubble-2 {
            position: fixed;
            bottom: 10%;
            right: 8%;
            width: 320px;
            height: 320px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(0, 245, 212, 0.3) 0%, rgba(56, 189, 248, 0.08) 70%, transparent 100%);
            filter: blur(45px);
            z-index: 0;
            pointer-events: none;
        }

        /* Rising Dark Purple Glass Form Card Container */
        div[data-testid="stForm"] {
            background: linear-gradient(145deg, rgba(24, 15, 46, 0.95) 0%, rgba(15, 9, 32, 0.98) 100%) !important;
            border-radius: 32px !important;
            padding: 30px 24px 26px 24px !important;
            box-shadow: 0 25px 65px rgba(0, 0, 0, 0.8), 0 0 35px rgba(168, 85, 247, 0.2) !important;
            border: 1.5px solid rgba(168, 85, 247, 0.35) !important;
            margin-top: 8px !important;
        }

        /* Input field labels & text */
        div[data-testid="stTextInput"] label p,
        div[data-testid="stSelectbox"] label p {
            color: #F8FAFC !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            margin-bottom: 2px !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"],
        div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        div[data-testid="stTextInput"] input {
            background-color: #100924 !important;
            background: #100924 !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            border: 1.5px solid rgba(168, 85, 247, 0.3) !important;
            border-radius: 16px !important;
            transition: all 0.2s ease !important;
            overflow: hidden !important;
        }

        div[data-testid="stTextInput"] input {
            border: none !important;
            font-size: 13.5px !important;
            font-weight: 600 !important;
            padding: 10px 14px !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: #00F5D4 !important;
            box-shadow: 0 0 0 3px rgba(0, 245, 212, 0.25) !important;
        }

        /* Password visibility eye button */
        div[data-testid="stTextInput"] button {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #A5B4FC !important;
        }

        /* Selectbox inside signup card */
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #100924 !important;
            background: #100924 !important;
            border: 1.5px solid rgba(168, 85, 247, 0.3) !important;
            border-radius: 16px !important;
            color: #FFFFFF !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 13.5px !important;
        }
        div[data-testid="stSelectbox"] svg {
            fill: #00F5D4 !important;
        }

        /* Checkbox label */
        div[data-testid="stCheckbox"] label span,
        div[data-testid="stCheckbox"] label p {
            color: #CBD5E1 !important;
            font-size: 12.5px !important;
            font-weight: 600 !important;
        }

        /* Secondary & Standard buttons on login page */
        div[data-testid="stButton"] button[kind="secondary"],
        div[data-testid="stButton"] button:not([kind="primary"]) {
            background-color: #160F2E !important;
            background: #160F2E !important;
            color: #F8FAFC !important;
            border: 1.5px solid rgba(168, 85, 247, 0.35) !important;
            border-radius: 25px !important;
            font-weight: 800 !important;
            font-size: 14px !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        div[data-testid="stButton"] button[kind="secondary"]:hover,
        div[data-testid="stButton"] button:not([kind="primary"]):hover {
            background-color: #1E143E !important;
            background: #1E143E !important;
            border-color: #00F5D4 !important;
            color: #00F5D4 !important;
            transform: translateY(-1.5px) !important;
            box-shadow: 0 8px 24px rgba(0, 245, 212, 0.25) !important;
        }

        div[data-testid="stButton"] button:not([kind="primary"]) p,
        div[data-testid="stButton"] button:not([kind="primary"]) span {
            color: #F8FAFC !important;
            font-weight: 800 !important;
        }

        div[data-testid="stButton"] button:not([kind="primary"]):hover p,
        div[data-testid="stButton"] button:not([kind="primary"]):hover span {
            color: #00F5D4 !important;
        }

        /* Primary gradient buttons: Amethyst to Electric Cyan */
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stForm"] button[kind="primary"] {
            background: linear-gradient(135deg, #A855F7 0%, #00F5D4 100%) !important;
            color: #090514 !important;
            border: none !important;
            border-radius: 26px !important;
            font-weight: 900 !important;
            font-size: 14.5px !important;
            box-shadow: 0 8px 25px rgba(0, 245, 212, 0.45) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        div[data-testid="stButton"] button[kind="primary"]:hover,
        div[data-testid="stForm"] button[kind="primary"]:hover {
            box-shadow: 0 12px 32px rgba(0, 245, 212, 0.65) !important;
            transform: translateY(-2px) scale(1.02) !important;
        }

        div[data-testid="stButton"] button[kind="primary"] p,
        div[data-testid="stButton"] button[kind="primary"] span,
        div[data-testid="stForm"] button[kind="primary"] p,
        div[data-testid="stForm"] button[kind="primary"] span {
            color: #090514 !important;
            font-weight: 900 !important;
        }

        /* Back Navigation button */
        .btn-back-pill button {
            max-width: 90px !important;
            background: #160F2E !important;
            border: 1px solid rgba(168, 85, 247, 0.4) !important;
            border-radius: 18px !important;
            color: #00F5D4 !important;
            font-weight: 700 !important;
            font-size: 12.5px !important;
            padding: 4px 12px !important;
        }
        .btn-back-pill button:hover {
            border-color: #00F5D4 !important;
            color: #00F5D4 !important;
        }
        </style>
        <div class="ambient-bubble-1"></div>
        <div class="ambient-bubble-2"></div>
        """),
        unsafe_allow_html=True
    )

    # =========================================================================
    # SCREEN 1: WELCOME SCREEN (Middle screen in user image)
    # =========================================================================
    if screen == "welcome":
        # Welcome illustration + titles
        st.markdown(
            textwrap.dedent("""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 12px;">
                <div style="font-size: 34px; font-weight: 900; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 8px; text-shadow: 0 0 20px rgba(0, 245, 212, 0.35);">
                    Welcome =)
                </div>
                <div style="font-size: 13.5px; color: #CBD5E1; font-weight: 500; line-height: 1.5; max-width: 340px; margin: 0 auto;">
                    Hi clinician! We're here to assist your clinical neuro-oncology workflow.<br>
                    The choice is yours: <b style="color: #00F5D4;">Log in</b> or <b style="color: #A855F7;">create an account</b>.
                </div>
            </div>

            <!-- Engaging Clinician & MRI Illustration in Deep Dark Cyber-Palette -->
            <div style="display: flex; justify-content: center; align-items: center; margin: 18px 0 24px 0;">
                <div style="width: 220px; height: 190px; background: radial-gradient(circle, rgba(168,85,247,0.25) 0%, rgba(0,245,212,0.1) 60%, transparent 100%);
                            border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative;">
                    <svg width="180" height="170" viewBox="0 0 180 170" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <!-- Floating Sparkles & Organic Blobs -->
                        <circle cx="30" cy="50" r="14" fill="#00F5D4" opacity="0.6"/>
                        <circle cx="150" cy="115" r="12" fill="#A855F7" opacity="0.6"/>
                        <path d="M145 40 L148 48 L156 51 L148 54 L145 62 L142 54 L134 51 L142 48 Z" fill="#00F5D4"/>
                        <path d="M25 125 L27 130 L32 132 L27 134 L25 139 L23 134 L18 132 L23 130 Z" fill="#A855F7"/>
                        <!-- Clinician Body & Tablet -->
                        <circle cx="90" cy="38" r="18" fill="#c084fc"/>
                        <path d="M82 28 C82 22 98 22 98 28 C98 33 93 35 90 35 C87 35 82 33 82 28 Z" fill="#160F2E"/>
                        <!-- Dark Purple / White Coat -->
                        <path d="M68 62 C68 52 112 52 112 62 L116 110 L64 110 Z" fill="#1E143E" stroke="#A855F7" stroke-width="1.5" filter="drop-shadow(0 4px 10px rgba(0,0,0,0.5))"/>
                        <path d="M85 58 L90 85 L95 58 Z" fill="#7928CA"/>
                        <circle cx="90" cy="68" r="4" fill="#00F5D4"/>
                        <!-- Stethoscope -->
                        <path d="M78 62 C78 76 86 82 90 82 C94 82 102 76 102 62" stroke="#00F5D4" stroke-width="2.5" stroke-linecap="round"/>
                        <!-- Legs / Trousers -->
                        <path d="M74 110 L78 155 L86 155 L87 110" fill="#160F2E"/>
                        <path d="M93 110 L94 155 L102 155 L106 110" fill="#160F2E"/>
                        <!-- Digital Diagnostics Tablet -->
                        <rect x="100" y="70" width="36" height="26" rx="4" fill="#090514" stroke="#00F5D4" stroke-width="1.5"/>
                        <circle cx="118" cy="83" r="6" fill="#00F5D4" opacity="0.9"/>
                        <path d="M106 77 H130 M106 89 H124" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )

        # Primary Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create Account", key="btn_welcome_signup", use_container_width=True, type="primary"):
                st.session_state["auth_screen"] = "signup"
                st.rerun()

        with col2:
            if st.button("Log In", key="btn_welcome_login", use_container_width=True, type="secondary"):
                st.session_state["auth_screen"] = "login"
                st.rerun()

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # 1-Click Instant Clinician Access Cards
        st.markdown(
            textwrap.dedent("""
            <div style="background: rgba(22, 14, 44, 0.85); backdrop-filter: blur(14px); border-radius: 24px;
                        padding: 16px; border: 1.5px solid rgba(168, 85, 247, 0.35); box-shadow: 0 12px 30px rgba(0, 0, 0, 0.7), 0 0 20px rgba(168, 85, 247, 0.2);">
                <div style="font-size: 11px; font-weight: 800; color: #00F5D4; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px; text-align: center; text-shadow: 0 0 10px rgba(0, 245, 212, 0.4);">
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

    # =========================================================================
    # SCREEN 2: LOGIN / "WELCOME BACK" (Left screen in user image)
    # =========================================================================
    elif screen == "login":
        # Top Navigation Bar with Back Button
        st.markdown("<div class='btn-back-pill'>", unsafe_allow_html=True)
        if st.button("‹ Back", key="btn_back_to_welcome_from_login"):
            st.session_state["auth_screen"] = "welcome"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        with st.form("form_login", clear_on_submit=False):
            st.markdown(
                textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 18px;">
                    <div style="font-size: 27px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.4px; text-shadow: 0 0 16px rgba(0, 245, 212, 0.35);">
                        Welcome Back
                    </div>
                    <div style="font-size: 13px; color: #CBD5E1; margin-top: 4px; line-height: 1.45;">
                        Ready to continue your diagnostic journey?<br>
                        Your clinical workstation is right here.
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
                remember = st.checkbox("Remember me", value=True)
            with col_forgot:
                st.markdown(
                    "<div style='text-align: right; padding-top: 4px;'>"
                    "<a href='#' style='color: #00F5D4; font-size: 11.5px; font-weight: 700; text-decoration: none; text-shadow: 0 0 8px rgba(0,245,212,0.4);'>"
                    "Forgot password?</a></div>",
                    unsafe_allow_html=True
                )

            submitted = st.form_submit_button("Log In", type="primary", use_container_width=True)

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
                        # Dynamic login fallback for custom clinical accounts
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

        # Divider & Social / SSO Sign-in
        st.markdown(
            textwrap.dedent("""
            <div style="display: flex; align-items: center; margin: 18px 0 14px 0; color: #A5B4FC; font-size: 11.5px; font-weight: 600;">
                <div style="flex: 1; height: 1px; background: rgba(168, 85, 247, 0.3);"></div>
                <div style="padding: 0 10px;">Sign in with</div>
                <div style="flex: 1; height: 1px; background: rgba(168, 85, 247, 0.3);"></div>
            </div>
            """),
            unsafe_allow_html=True
        )

        s1, s2, s3 = st.columns(3)
        with s1:
            if st.button("🌐 Google", key="sso_google", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                st.rerun()
        with s2:
            if st.button("🍎 Apple", key="sso_apple", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.sharma@neuroscan.ai"]
                st.rerun()
        with s3:
            if st.button("🏥 PACS ID", key="sso_pacs", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["leonba@pixel.co.id"]
                st.rerun()

        # Switch to Sign Up
        st.markdown("<div style='margin-top: 14px; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Don't have an account? Sign Up", key="btn_goto_signup", use_container_width=True):
            st.session_state["auth_screen"] = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SCREEN 3: SIGN UP / "CREATE YOUR ACCOUNT" (Right screen in user image)
    # =========================================================================
    elif screen == "signup":
        # Top Navigation Bar with Back Button
        st.markdown("<div class='btn-back-pill'>", unsafe_allow_html=True)
        if st.button("‹ Back", key="btn_back_to_welcome_from_signup"):
            st.session_state["auth_screen"] = "welcome"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        with st.form("form_signup", clear_on_submit=False):
            st.markdown(
                textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 18px;">
                    <div style="font-size: 27px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.4px; text-shadow: 0 0 16px rgba(0, 245, 212, 0.35);">
                        Create Your Account
                    </div>
                    <div style="font-size: 13px; color: #CBD5E1; margin-top: 4px; line-height: 1.45;">
                        Register your clinical credentials to access<br>
                        FDA SaMD Class II diagnostic tools.
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )

            full_name = st.text_input("Full Name", placeholder="Enter full name (e.g. Dr. Emily Vance)")
            email = st.text_input("Clinical Email", placeholder="Enter clinical email")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            specialty = st.selectbox(
                "Clinical Department",
                ["Neuro-Radiology", "Neurosurgery", "Clinical Neurology", "Medical Physics & AI"]
            )
            terms = st.checkbox("I agree to HIPAA Safe Harbor and clinical AI protocol terms", value=True)

            submitted = st.form_submit_button("Get Started", type="primary", use_container_width=True)

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

        # Divider & Social / SSO Sign-up
        st.markdown(
            textwrap.dedent("""
            <div style="display: flex; align-items: center; margin: 18px 0 14px 0; color: #A5B4FC; font-size: 11.5px; font-weight: 600;">
                <div style="flex: 1; height: 1px; background: rgba(168, 85, 247, 0.3);"></div>
                <div style="padding: 0 10px;">Sign up with</div>
                <div style="flex: 1; height: 1px; background: rgba(168, 85, 247, 0.3);"></div>
            </div>
            """),
            unsafe_allow_html=True
        )

        su1, su2, su3 = st.columns(3)
        with su1:
            if st.button("🌐 Google", key="sso_up_google", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]
                st.rerun()
        with su2:
            if st.button("🍎 Apple", key="sso_up_apple", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["dr.sharma@neuroscan.ai"]
                st.rerun()
        with su3:
            if st.button("🏥 PACS ID", key="sso_up_pacs", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user"] = CLINICAL_USERS["leonba@pixel.co.id"]
                st.rerun()

        # Switch to Log In
        st.markdown("<div style='margin-top: 14px; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Already have an account? Log In", key="btn_goto_login", use_container_width=True):
            st.session_state["auth_screen"] = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
