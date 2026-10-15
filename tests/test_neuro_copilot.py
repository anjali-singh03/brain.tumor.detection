# test_neuro_copilot.py
# Unit tests for NeuroCopilot surgical resectability engine and survival projection
import unittest
from src.neuro_copilot import (
    calculate_surgical_risk,
    render_risk_radar,
    render_survival_trajectory
)


class TestNeuroCopilot(unittest.TestCase):
    def test_calculate_surgical_risk_glioma(self):
        risk = calculate_surgical_risk(
            tumor_class="glioma",
            volume_cm3=14.5,
            eloquent_proximity="Adjacent (Within 5mm)",
            vascular_encasement=True
        )
        self.assertIn("WHO Grade", risk["who_grade"])
        self.assertIsInstance(risk["resectability_pct"], float)
        self.assertGreater(risk["resectability_pct"], 0)
        self.assertLessEqual(risk["resectability_pct"], 100)
        self.assertIn("IDH1/2 Mutation", risk["molecular_markers"])

    def test_calculate_surgical_risk_notumor(self):
        risk = calculate_surgical_risk(tumor_class="notumor", volume_cm3=0.0)
        self.assertEqual(risk["resectability_pct"], 100.0)
        self.assertEqual(risk["projected_postop_kps"], 100)

    def test_render_risk_radar(self):
        risk = calculate_surgical_risk("meningioma", 12.0)
        fig = render_risk_radar(risk["risk_scores"])
        self.assertIsNotNone(fig)

    def test_render_survival_trajectory(self):
        fig = render_survival_trajectory("glioma", 75.0)
        self.assertIsNotNone(fig)


if __name__ == "__main__":
    unittest.main()
