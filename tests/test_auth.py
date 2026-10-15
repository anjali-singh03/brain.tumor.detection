# test_auth.py
# Unit tests for the authentication and session management module
import unittest
from unittest.mock import MagicMock
from src.auth import (
    hash_password,
    is_authenticated,
    get_current_user,
    logout_user,
    CLINICAL_USERS
)


class TestAuthModule(unittest.TestCase):
    def test_hash_password(self):
        h1 = hash_password("DemoMedical2026!")
        h2 = hash_password("DemoMedical2026!")
        h3 = hash_password("DifferentPassword")
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)
        self.assertEqual(len(h1), 64)

    def test_pre_registered_users_exist(self):
        self.assertIn("dr.mitchell@neuroscan.ai", CLINICAL_USERS)
        self.assertIn("dr.sharma@neuroscan.ai", CLINICAL_USERS)
        self.assertIn("leonba@pixel.co.id", CLINICAL_USERS)

    def test_authentication_flow(self):
        import streamlit as st
        # Simulate session state
        st.session_state["authenticated"] = True
        st.session_state["user"] = CLINICAL_USERS["dr.mitchell@neuroscan.ai"]

        self.assertTrue(is_authenticated())
        user = get_current_user()
        self.assertEqual(user["name"], "Dr. Sarah Mitchell")
        self.assertEqual(user["role"], "Senior Radiologist")

    def test_default_unauthenticated_state(self):
        import streamlit as st
        st.session_state["authenticated"] = False
        st.session_state["user"] = None

        self.assertFalse(is_authenticated())
        user = get_current_user()
        self.assertEqual(user["name"], "Guest Clinician")


if __name__ == "__main__":
    unittest.main()
