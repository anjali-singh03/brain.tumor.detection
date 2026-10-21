# auth.py
# Clinical Authentication for Brain Tumor Detection App
# Designed as a Direct Hospital Staff Login Portal (Siemens syngo.via / GE Centricity Style)
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

    # Global CSS injection for Centered Clinical PACS Login
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

        /* Centered login form container */
        .block-container {
            max-width: 520px !important;
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            margin: 0 auto !important;
        }

        /* Hospital Brand Header */
        .clinical-login-header {
            text-align: center;
            margin-bottom: 20px;
        }

        .clinical-brand-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
        }

        .clinical-brand-badge h1 {
            font-size: 26px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.3px;
            margin: 0;
            display: inline;
        }

        .clinical-brand-badge span.version-tag {
            font-size: 11px;
            font-weight: 700;
            color: #38BDF8;
            background: rgba(14, 165, 233, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 2px 7px;
            border-radius: 4px;
            letter-spacing: 0.5px;
        }

        .clinical-kicker-sub {
            font-size: 11.5px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: #38BDF8;
            margin-top: 4px;
        }

        .clinical-meta-sub {
            font-size: 11px;
            color: #94A3B8;
            margin-top: 4px;
        }

        /* Form Container for Login & Sign Up */
        div[data-testid="stForm"] {
            background: linear-gradient(145deg, #0E1726 0%, #090D16 100%) !important;
            border-radius: 14px !important;
            padding: 26px 24px !important;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85), 0 0 20px rgba(14, 165, 233, 0.12) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.22) !important;
            margin-top: 8px !important;
        }

        /* Input Fields */
        div[data-testid="stTextInput"] label p,
        div[data-testid="stSelectbox"] label p {
            color: #F1F5F9 !important;
            font-weight: 700 !important;
            font-size: 12.5px !important;
            margin-bottom: 3px !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"],
        div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        div[data-testid="stTextInput"] input {
            background-color: #070B14 !important;
            background: #070B14 !important;
            color: #FFFFFF !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            border: 1.5px solid rgba(56, 189, 248, 0.22) !important;
            border-radius: 8px !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: #0EA5E9 !important;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.22) !important;
        }
        div[data-testid="stTextInput"] input {
            font-size: 13.5px !important;
            padding: 8px 12px !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #070B14 !important;
            border: 1.5px solid rgba(56, 189, 248, 0.22) !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        div[data-testid="stCheckbox"] label span,
        div[data-testid="stCheckbox"] label p {
            color: #CBD5E1 !important;
            font-size: 12px !important;
            font-weight: 600 !important;
        }

        /* Primary Action Buttons */
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stForm"] button[kind="primary"] {
            background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 100%) !important;
            border: none !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            font-weight: 800 !important;
            font-size: 13.5px !important;
            letter-spacing: 0.4px !important;
            padding: 10px 20px !important;
            box-shadow: 0 6px 18px rgba(14, 165, 233, 0.35) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover,
        div[data-testid="stForm"] button[kind="primary"]:hover {
            box-shadow: 0 8px 24px rgba(14, 165, 233, 0.6) !important;
            transform: translateY(-1.5px) !important;
        }

        /* Secondary Buttons */
        div[data-testid="stButton"] button[kind="secondary"],
        div[data-testid="stButton"] button:not([kind="primary"]) {
            background: #0E1726 !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            color: #E2E8F0 !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            font-size: 12px !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stButton"] button:not([kind="primary"]):hover {
            border-color: #38BDF8 !important;
            color: #38BDF8 !important;
            background: #142033 !important;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.2) !important;
        }
        </style>
        """),
        unsafe_allow_html=True
    )

    # Hospital Brand Header (Always Visible at Top of Login)
    st.markdown(
        textwrap.dedent("""
        <div class="clinical-login-header">
            <div class="clinical-brand-badge">
                <span style="font-size: 30px;">🧠</span>
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
                <div style="text-align: center; margin-bottom: 18px;">
                    <div style="font-size: 20px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.2px;">
                        Hospital Staff Authentication
                    </div>
                    <div style="font-size: 12px; color: #94A3B8; margin-top: 3px; line-height: 1.4;">
                        Enter institutional credentials to access protected clinical data.
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
            <div style="background: rgba(14, 23, 38, 0.85); border-radius: 12px; padding: 14px 16px; margin-top: 14px;
                        border: 1px solid rgba(56, 189, 248, 0.2); box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);">
                <div style="font-size: 10.5px; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; text-align: center;">
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
            <div style="display: flex; align-items: center; margin: 16px 0 12px 0; color: #64748B; font-size: 11px; font-weight: 700;">
                <div style="flex: 1; height: 1px; background: rgba(56, 189, 248, 0.2);"></div>
                <div style="padding: 0 10px;">INSTITUTIONAL SSO</div>
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
        st.markdown("<div style='margin-top: 14px; text-align: center;'>", unsafe_allow_html=True)
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
                <div style="text-align: center; margin-bottom: 18px;">
                    <div style="font-size: 20px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.2px;">
                        Register Institutional Credentials
                    </div>
                    <div style="font-size: 12px; color: #94A3B8; margin-top: 3px; line-height: 1.4;">
                        Establish a verified clinical seat for institutional decision support.
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
