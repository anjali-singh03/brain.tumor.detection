# test_fhir.py
# Unit tests for HL7 FHIR DiagnosticReport resource generation
import unittest
import json
from src.fhir_exporter import generate_fhir_diagnostic_report


class TestFhirExporter(unittest.TestCase):
    def test_generate_fhir_report_valid_json(self):
        recist = {
            "recist_category": "Measurable Target Lesion (RECIST 1.1)",
            "volume_cm3": 14.5,
            "max_diameter_mm": 26.2,
            "mass_effect": "Mild midline shift"
        }
        json_str = generate_fhir_diagnostic_report(
            patient_token="PX-12345",
            accession_no="ACC-9988",
            predicted_condition="glioma",
            confidence=91.4,
            recist_metrics=recist,
            clinician_name="Dr. Sarah Mitchell"
        )

        data = json.loads(json_str)
        self.assertEqual(data["resourceType"], "DiagnosticReport")
        self.assertEqual(data["status"], "final")
        self.assertIn("PX-12345", data["subject"]["reference"])
        self.assertIn("ACC-9988", data["imagingStudy"][0]["identifier"]["value"])
        self.assertEqual(len(data["conclusionCode"][0]["coding"]), 1)
        self.assertEqual(data["conclusionCode"][0]["coding"][0]["code"], "44445000")  # SNOMED Glioma

    def test_fhir_normal_study(self):
        recist = {
            "recist_category": "Complete Response / Clear Parenchyma",
            "volume_cm3": 0.0,
            "max_diameter_mm": 0.0,
            "mass_effect": "None"
        }
        json_str = generate_fhir_diagnostic_report(
            patient_token="PX-NORMAL",
            accession_no="ACC-0001",
            predicted_condition="notumor",
            confidence=99.8,
            recist_metrics=recist
        )

        data = json.loads(json_str)
        self.assertEqual(data["conclusionCode"][0]["coding"][0]["code"], "17621005")  # Normal


if __name__ == "__main__":
    unittest.main()
