"""
test_report_generator.py
Tests for the PDF report generator.
"""
import os
import tempfile

from src.report_generator import create_pdf_report


class TestCreatePdfReport:
    """Tests for create_pdf_report in report_generator.py."""

    def test_creates_file(self):
        """Report file must exist after calling create_pdf_report."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.pdf")
            create_pdf_report("Glioma", 92.5, "A tumor in glial cells.", path)
            assert os.path.isfile(path), "PDF file was not created."

    def test_file_is_nonempty(self):
        """The generated PDF must not be empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.pdf")
            create_pdf_report("Meningioma", 75.0, "A benign meningeal tumor.", path)
            assert os.path.getsize(path) > 0, "PDF file is empty."

    def test_file_starts_with_pdf_header(self):
        """Valid PDFs must start with the %PDF magic bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.pdf")
            create_pdf_report("No Tumor Detected", 98.1, "No tumor found.", path)
            with open(path, "rb") as f:
                header = f.read(4)
            assert header == b"%PDF", f"File does not start with %PDF header: {header!r}"

    def test_returns_filepath(self):
        """create_pdf_report must return the path it wrote to."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.pdf")
            result = create_pdf_report("Pituitary Tumor", 88.3, "A pituitary adenoma.", path)
            assert result == path

    def test_long_overview_does_not_raise(self):
        """Very long overview text should not crash the PDF generator."""
        long_text = "Detail. " * 500  # ~4 000 chars
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.pdf")
            create_pdf_report("Glioma", 65.0, long_text, path)
            assert os.path.isfile(path)

    def test_special_characters_in_title(self):
        """Special characters in the prediction title must not crash the generator."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.pdf")
            create_pdf_report("Tumor (Grade II) — Low-Risk", 55.5, "Overview.", path)
            assert os.path.isfile(path)

    def test_zero_confidence(self):
        """Confidence of 0% is an edge case that must be handled gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.pdf")
            create_pdf_report("Glioma", 0.0, "Low confidence result.", path)
            assert os.path.isfile(path)

    def test_full_confidence(self):
        """Confidence of 100% is an edge case that must be handled gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.pdf")
            create_pdf_report("No Tumor Detected", 100.0, "Very high confidence.", path)
            assert os.path.isfile(path)
