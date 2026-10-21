# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- **Batch Processing**: Upload multiple scans and export predictions as CSV.
- **Compare Scans**: Side-by-side comparison of two MRI images and their predictions.
- **Grad-CAM**: Visual overlay explaining the model's focus points.
- **PDF Export**: Generate and download a PDF report containing the prediction, confidence, and medical info.
- **Language Toggle**: Added a Hindi translation toggle for UI components.
- **Automated Tests**: Pytest suite checking model validity, input constraints, and dictionary parity.
- **Training Script**: A new `train.py` script for Kaggle execution featuring stratified splits, augmentation, and class weighting.
- **CI/CD**: Added GitHub Actions workflow.
- **Docker**: Added `Dockerfile` for containerized deployments.

### Changed
- **Editorial Bioluminescent Iris & Obsidian Theme**: Redesigned authentication showcase and clinical workstation adhering to the high-fashion editorial aesthetic ("A Deeper Kind of Precision"). Includes deep obsidian midnight palette (`#030206`), electric cyan (`#00D2FF`) and royal iris violet (`#8A2BE2`) glowing telemetry, `Playfair Display` serif typography with italic ligatures, numbered editorial indices (`01 ——`, `02 ——`, `03 ——`), minimalist outline pill buttons (`EXPLORE WORKSTATION ——>`), and animated laser scanlines.
- **Architecture Refactor**: Split the monolithic `braintumorapp.py` into distinct logical modules (`inference.py`, `ui_components.py`, `content.py`, etc.).
- **UI Refresh**: Modernized CSS with better color contrast, shadows, and spacing for accessibility.

### Security
- **EXIF Stripping**: Image metadata is automatically stripped during validation to protect user privacy.
- **In-Memory Processing**: Images are no longer temporarily saved to disk.
- **Dependencies**: Pinned specific known-to-work versions in `requirements.txt`.
