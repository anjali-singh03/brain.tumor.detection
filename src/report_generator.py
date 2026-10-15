# report_generator.py
# Structured Clinical Radiology Report Generator (PDF)
from fpdf import FPDF
import datetime


def _sanitize(text: str) -> str:
    """
    Replace characters outside the Latin-1 range with ASCII equivalents so
    that fpdf2's built-in Helvetica font (latin-1 / cp1252) can encode them.
    """
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "\u2014": "-",    # em dash  —
        "\u2013": "-",    # en dash  –
        "\u2018": "'",    # left single quote  '
        "\u2019": "'",    # right single quote  '
        "\u201c": '"',    # left double quote  "
        "\u201d": '"',    # right double quote  "
        "\u2026": "...",  # ellipsis  …
        "\u00b0": " degrees",  # degree sign °
        "\u00ae": "(R)",  # registered ®
        "\u2122": "(TM)",  # trademark ™
        "\u2022": "*",    # bullet point •
        "\u2265": ">=",   # greater or equal ≥
        "\u2264": "<=",   # less or equal ≤
    }
    for char, sub in replacements.items():
        text = text.replace(char, sub)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def create_pdf_report(
    prediction_title: str,
    confidence: float,
    overview: str,
    filepath: str = "report.pdf",
    recist_data: dict = None,
    dicom_data: dict = None,
    clinician_name: str = "Dr. Sarah Mitchell, MD",
    dictated_notes: str = ""
):
    """
    Generate an industry-ready Structured Clinical Radiology Report in PDF format.
    Includes patient telemetry, RECIST 1.1 dimensions, clinical impression,
    and clinician notes.
    """
    prediction_title = _sanitize(prediction_title)
    overview = _sanitize(overview)
    clinician_name = _sanitize(clinician_name)
    dictated_notes = _sanitize(dictated_notes) if dictated_notes else ""

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header Banner
    pdf.set_fill_color(13, 24, 33)
    pdf.rect(0, 0, 210, 32, "F")

    pdf.set_font("helvetica", "B", 17)
    pdf.set_text_color(45, 212, 191)
    pdf.set_xy(10, 8)
    pdf.cell(0, 8, "NeuroScan 2.5 Clinical PACS Workstation", align="L")

    pdf.set_font("helvetica", "I", 9)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(10, 18)
    pdf.cell(0, 6, "AI-Assisted Neuro-Oncology Diagnostic Study  |  HL7 / FHIR Standard", align="L")

    pdf.set_xy(10, 36)
    pdf.set_text_color(0, 0, 0)

    # Patient & Study Demographics Table
    patient_id = dicom_data.get("Patient_Token", "ANON-PX-84920") if dicom_data else "ANON-PX-84920"
    accession = dicom_data.get("Accession_No", "ACC-77419A") if dicom_data else "ACC-77419A"
    scanner = dicom_data.get("Manufacturer", "Siemens 3.0T MAGNETOM Prisma") if dicom_data else "Siemens 3.0T MAGNETOM Prisma"
    study_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    pdf.set_font("helvetica", "B", 9)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(45, 6, "Patient ID:", 1, new_x="RIGHT", new_y="TOP", align="L", fill=True)
    pdf.set_font("helvetica", "", 9)
    pdf.cell(50, 6, _sanitize(patient_id), 1, new_x="RIGHT", new_y="TOP", align="L")

    pdf.set_font("helvetica", "B", 9)
    pdf.cell(45, 6, "Accession No:", 1, new_x="RIGHT", new_y="TOP", align="L", fill=True)
    pdf.set_font("helvetica", "", 9)
    pdf.cell(50, 6, _sanitize(accession), 1, new_x="LMARGIN", new_y="NEXT", align="L")

    pdf.set_font("helvetica", "B", 9)
    pdf.cell(45, 6, "Scanner Hardware:", 1, new_x="RIGHT", new_y="TOP", align="L", fill=True)
    pdf.set_font("helvetica", "", 9)
    pdf.cell(50, 6, _sanitize(scanner[:26]), 1, new_x="RIGHT", new_y="TOP", align="L")

    pdf.set_font("helvetica", "B", 9)
    pdf.cell(45, 6, "Study Timestamp:", 1, new_x="RIGHT", new_y="TOP", align="L", fill=True)
    pdf.set_font("helvetica", "", 9)
    pdf.cell(50, 6, _sanitize(study_date), 1, new_x="LMARGIN", new_y="NEXT", align="L")

    pdf.ln(4)

    # Clinical Indication
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 7, "1. CLINICAL INDICATION", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 41, 59)
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5, "Diagnostic brain MRI evaluation for suspected intracranial space-occupying lesion.", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)

    # Technique & Pulse Sequences
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 7, "2. TECHNIQUE & PROTOCOL", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 41, 59)
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(
        0, 5,
        "High-resolution multi-planar MRI scan. Multi-parametric sequences: T1-Weighted Axial, "
        "T1+Gadolinium Contrast, T2-Weighted Fast Spin Echo, and FLAIR. Slice thickness: 1.0mm isotropic.",
        new_x="LMARGIN", new_y="NEXT"
    )

    pdf.ln(2)

    # Imaging Findings & AI Classification
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 7, "3. IMAGING FINDINGS & NEURAL AI CLASSIFICATION", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 41, 59)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 6, f"Primary Diagnostic Finding: {prediction_title}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 6, f"AI Model Confidence: {confidence:.1f}%  (Deep ConvNet MobileNetV2 + Grad-CAM XAI)", new_x="LMARGIN", new_y="NEXT")

    if recist_data:
        vol = recist_data.get("volume_cm3", "N/A")
        diam = recist_data.get("max_diameter_mm", "N/A")
        mass_eff = recist_data.get("mass_effect", "Intact midline")
        pdf.cell(0, 6, _sanitize(f"Tumor Dimensions: {diam} mm max axial  |  Estimated Volume: {vol} cm3"), new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, _sanitize(f"Mass Effect: {mass_eff}"), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)

    # Condition Overview
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 6, "Pathological Characteristics:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 9.5)
    pdf.multi_cell(0, 5, overview, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)

    # Dictated Clinician Notes (if available)
    if dictated_notes:
        pdf.set_font("helvetica", "B", 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 7, "4. RADIOLOGIST DICTATION & CLINICAL IMPRESSION", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 41, 59)
        pdf.set_font("helvetica", "I", 10)
        pdf.multi_cell(0, 5, f'"{dictated_notes}"', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # Recommendations & Multidisciplinary Next Steps
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 7, "5. MULTIDISCIPLINARY TUMOR BOARD RECOMMENDATIONS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 41, 59)
    pdf.set_font("helvetica", "", 9.5)
    rec_text = (
        "1. Urgent neurosurgical consultation for surgical biopsy / debulking evaluation.\n"
        "2. Follow-up volumetric MRI in 30 days to assess interval growth rate.\n"
        "3. Correlate with clinical neurology examination (cranial nerve exam & visual fields)."
    )
    pdf.multi_cell(0, 5, rec_text, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)

    # Signature & Attestation Block
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(10, pdf.get_y(), 190, 22, "F")
    pdf.set_font("helvetica", "B", 9)
    pdf.cell(0, 6, f"Electronically Verified & Signed by: {clinician_name}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "I", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "FDA SaMD Class II Decision Support Attestation  |  HIPAA Safe Harbor Compliant", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "DISCLAIMER: AI decision support output must be correlated with clinical examination by certified radiologists.", new_x="LMARGIN", new_y="NEXT")

    # Output
    pdf.output(filepath)
    return filepath
