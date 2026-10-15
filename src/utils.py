import logging


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with basic configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(name)


def setup_app_state(st_module):
    """Initialize streamlit session state variables if needed."""
    if "threshold" not in st_module.session_state:
        st_module.session_state["threshold"] = 70
    if "lang" not in st_module.session_state:
        st_module.session_state["lang"] = "en"
    if "history" not in st_module.session_state:
        st_module.session_state["history"] = []
    if "authenticated" not in st_module.session_state:
        st_module.session_state["authenticated"] = False
    if "user" not in st_module.session_state:
        st_module.session_state["user"] = None
    if "auth_mode" not in st_module.session_state:
        st_module.session_state["auth_mode"] = "login"

