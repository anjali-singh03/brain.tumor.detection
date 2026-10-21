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
- **Clinical PACS Enterprise Theme**: Redesigned application into an authentic, hospital-grade Clinical PACS Workstation (Siemens / GE Healthcare / Epic style). Replaced fashion editorial portrait with a high-precision Siemens MAGNETOM Skyra 3.0T DICOM HUD preview, removed all ECG wave lines across telemetry and workstation bars, added 100% interactive clickable top navigation controls, and applied deep surgical slate (`#090D16`), container slate (`#0E1726`), and clinical blue/cyan (`#0EA5E9` / `#38BDF8`) accents with clean medical typography (`Plus Jakarta Sans` and `JetBrains Mono`).
- **Architecture Refactor**: Split the monolithic `braintumorapp.py` into distinct logical modules (`inference.py`, `ui_components.py`, `content.py`, etc.).
- **UI Refresh**: Modernized CSS with better color contrast, shadows, and spacing for accessibility.

### Security
- **EXIF Stripping**: Image metadata is automatically stripped during validation to protect user privacy.
- **In-Memory Processing**: Images are no longer temporarily saved to disk.
- **Dependencies**: Pinned specific known-to-work versions in `requirements.txt`.
