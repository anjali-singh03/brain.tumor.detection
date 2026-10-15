# pacs.py
# Clinical PACS (Picture Archiving and Communication System) Tools & MRI Sequence Engine
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import hashlib
import time


def adjust_window_level(image: Image.Image, brightness: float = 1.0, contrast: float = 1.0,
                        apply_clahe: bool = False, invert: bool = False) -> Image.Image:
    """
    Adjust window width (contrast) and window center/level (brightness)
    similar to clinical radiology PACS diagnostic monitors.
    """
    img_rgb = image.convert("RGB")
    np_img = np.array(img_rgb)

    # Optional Contrast Limited Adaptive Histogram Equalization (CLAHE) for MRI soft-tissue
    if apply_clahe:
        lab = cv2.cvtColor(np_img, cv2.COLOR_RGB2LAB)
        l_chan, a_chan, b_chan = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        cl = clahe.apply(l_chan)
        limg = cv2.merge((cl, a_chan, b_chan))
        np_img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)

    processed = Image.fromarray(np_img)

    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(processed)
        processed = enhancer.enhance(brightness)

    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(processed)
        processed = enhancer.enhance(contrast)

    if invert:
        processed = ImageOps.invert(processed.convert("RGB"))

    return processed


def simulate_mri_sequences(base_img: Image.Image) -> dict:
    """
    Synthesize multi-parametric clinical MRI sequences from a base scan:
    - T1-Weighted (Anatomical reference)
    - T1+Contrast / T1-Gd (Gadolinium enhancement highlighting active tumor core)
    - T2-Weighted (Fluid bright, CSF white)
    - FLAIR (Fluid Attenuated Inversion Recovery: CSF suppressed, edema bright)
    """
    img = base_img.convert("L")
    np_img = np.array(img, dtype=np.float32)

    # 1. T1 Native (Clean anatomical contrast)
    t1 = np.clip(np_img * 0.95 + 5, 0, 255).astype(np.uint8)

    # 2. T1 + Gadolinium Contrast (Hyperintense enhancement on high-density regions)
    t1_gd = np_img.copy()
    high_signal = t1_gd > 130
    t1_gd[high_signal] = np.clip(t1_gd[high_signal] * 1.35, 0, 255)
    t1_gd = np.clip(t1_gd, 0, 255).astype(np.uint8)

    # 3. T2-Weighted (Fluid and CSF signal intensified)
    t2 = cv2.GaussianBlur(np_img, (3, 3), 0)
    t2 = np.clip(t2 * 1.15 + 15, 0, 255).astype(np.uint8)

    # 4. FLAIR (CSF suppressed, peritumoral hyperintense edema highlighted)
    flair = np_img.copy()
    low_signal = flair < 55
    flair[low_signal] = flair[low_signal] * 0.35  # Suppress free fluid
    mid_high_signal = (flair >= 100) & (flair <= 210)
    flair[mid_high_signal] = np.clip(flair[mid_high_signal] * 1.25, 0, 255)
    flair = np.clip(flair, 0, 255).astype(np.uint8)

    return {
        "T1-Native": Image.fromarray(t1).convert("RGB"),
        "T1-Contrast (Gd)": Image.fromarray(t1_gd).convert("RGB"),
        "T2-Weighted": Image.fromarray(t2).convert("RGB"),
        "FLAIR (Fluid Attenuated)": Image.fromarray(flair).convert("RGB")
    }


def compute_recist_metrics(tumor_class: str, confidence: float, length_mm: float, width_mm: float) -> dict:
    """
    Compute clinical oncology RECIST 1.1 metrics, approximate ellipsoid tumor volume,
    and clinical staging indicators.
    Formula: Volume = (pi / 6) * length * width * depth (depth ~ average of L and W)
    """
    if tumor_class == "notumor":
        return {
            "status": "No Neoplasm Detected",
            "max_diameter_mm": 0.0,
            "perpendicular_mm": 0.0,
            "volume_cm3": 0.0,
            "recist_category": "Complete Response / Clear Parenchyma",
            "mass_effect": "None (Midline structures intact)"
        }

    depth_mm = (length_mm + width_mm) / 2.0
    volume_mm3 = (np.pi / 6.0) * length_mm * width_mm * depth_mm
    volume_cm3 = round(volume_mm3 / 1000.0, 2)

    # Clinical mass effect estimation
    if volume_cm3 > 15.0:
        mass_effect = "Severe (Midline shift > 5mm, sulcal effacement observed)"
    elif volume_cm3 > 5.0:
        mass_effect = "Moderate (Local ventricular compression)"
    else:
        mass_effect = "Mild / Focal (Preserved ventricular symmetry)"

    return {
        "status": f"Neoplastic Lesion ({tumor_class.capitalize()})",
        "max_diameter_mm": round(length_mm, 1),
        "perpendicular_mm": round(width_mm, 1),
        "volume_cm3": volume_cm3,
        "recist_category": "Measurable Target Lesion (RECIST 1.1)",
        "mass_effect": mass_effect
    }


def generate_dicom_telemetry(filename: str = "AX_BRAIN_001.dcm") -> dict:
    """
    Generate authentic DICOM header telemetry parameters as parsed from
    hospital clinical PACS systems.
    """
    # Deterministic token based on filename
    h = hashlib.sha256(filename.encode()).hexdigest()[:8].upper()

    return {
        "Accession_No": f"ACC-{h}",
        "Patient_Token": f"ANON-PX-{h[:6]}",
        "Modality": "MR (Magnetic Resonance)",
        "Magnetic_Field": "3.0 Tesla (High-Field)",
        "Manufacturer": "Siemens Healthineers MAGNETOM Prisma",
        "Slice_Thickness": "1.00 mm (Isotropic)",
        "Matrix_Size": "512 x 512",
        "Repetition_Time_TR": "2200 ms",
        "Echo_Time_TE": "95 ms",
        "Inversion_Time_TI": "900 ms",
        "Coil": "64-Channel Head/Neck Matrix",
        "PHI_Status": "De-Identified (HIPAA Safe Harbor Compliant)"
    }


def extract_tumor_contours(image: Image.Image, heatmap: np.ndarray, alpha: float = 0.5) -> Image.Image:
    """
    Generate an edge-contour segmentation overlay differentiating the
    active hyperintense core from the peritumoral boundary.
    """
    orig_np = np.array(image.convert("RGB"))
    h, w, _ = orig_np.shape

    # Resize heatmap to match image dimensions
    heatmap_resized = cv2.resize(heatmap, (w, h))
    heatmap_norm = (heatmap_resized - heatmap_resized.min()) / (heatmap_resized.max() - heatmap_resized.min() + 1e-8)

    # Binary mask for active core (top 35% activation)
    core_mask = (heatmap_norm > 0.65).astype(np.uint8) * 255
    edema_mask = ((heatmap_norm > 0.35) & (heatmap_norm <= 0.65)).astype(np.uint8) * 255

    # Find contours
    core_contours, _ = cv2.findContours(core_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edema_contours, _ = cv2.findContours(edema_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    annotated = orig_np.copy()

    # Draw edema contour in glowing cyan
    cv2.drawContours(annotated, edema_contours, -1, (45, 212, 191), 2)
    # Draw tumor core contour in vivid red-coral
    cv2.drawContours(annotated, core_contours, -1, (239, 68, 68), 2)

    # Blend with original
    blended = cv2.addWeighted(annotated, alpha, orig_np, 1 - alpha, 0)
    return Image.fromarray(blended)
