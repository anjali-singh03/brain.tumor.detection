# test_pacs.py
# Unit tests for PACS image adjustments, multi-sequence MRI synthesis, and RECIST metrics
import unittest
from PIL import Image
import numpy as np
from src.pacs import (
    adjust_window_level,
    simulate_mri_sequences,
    compute_recist_metrics,
    generate_dicom_telemetry,
    extract_tumor_contours
)


class TestPacsModule(unittest.TestCase):
    def setUp(self):
        # Create a synthetic 100x100 grayscale image
        arr = np.zeros((100, 100), dtype=np.uint8)
        arr[30:70, 30:70] = 180  # simulated hyperintense lesion
        self.img = Image.fromarray(arr).convert("RGB")
        self.heatmap = np.zeros((10, 10), dtype=np.float32)
        self.heatmap[3:7, 3:7] = 0.9

    def test_adjust_window_level(self):
        res = adjust_window_level(self.img, brightness=1.2, contrast=1.3, apply_clahe=True, invert=True)
        self.assertIsInstance(res, Image.Image)
        self.assertEqual(res.size, (100, 100))

    def test_simulate_mri_sequences(self):
        seqs = simulate_mri_sequences(self.img)
        self.assertIn("T1-Native", seqs)
        self.assertIn("T1-Contrast (Gd)", seqs)
        self.assertIn("T2-Weighted", seqs)
        self.assertIn("FLAIR (Fluid Attenuated)", seqs)
        for s in seqs.values():
            self.assertIsInstance(s, Image.Image)
            self.assertEqual(s.size, (100, 100))

    def test_compute_recist_metrics_tumor(self):
        metrics = compute_recist_metrics("glioma", 85.0, 25.0, 15.0)
        self.assertEqual(metrics["max_diameter_mm"], 25.0)
        self.assertGreater(metrics["volume_cm3"], 0.0)
        self.assertEqual(metrics["recist_category"], "Measurable Target Lesion (RECIST 1.1)")

    def test_compute_recist_metrics_notumor(self):
        metrics = compute_recist_metrics("notumor", 99.0, 0.0, 0.0)
        self.assertEqual(metrics["volume_cm3"], 0.0)
        self.assertEqual(metrics["max_diameter_mm"], 0.0)
        self.assertIn("Clear Parenchyma", metrics["recist_category"])

    def test_generate_dicom_telemetry(self):
        telem = generate_dicom_telemetry("SCAN_123.dcm")
        self.assertIn("Patient_Token", telem)
        self.assertIn("Magnetic_Field", telem)
        self.assertEqual(telem["Modality"], "MR (Magnetic Resonance)")

    def test_extract_tumor_contours(self):
        contour_img = extract_tumor_contours(self.img, self.heatmap, alpha=0.5)
        self.assertIsInstance(contour_img, Image.Image)
        self.assertEqual(contour_img.size, (100, 100))


if __name__ == "__main__":
    unittest.main()
