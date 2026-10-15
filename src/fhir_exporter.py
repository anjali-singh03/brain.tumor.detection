# fhir_exporter.py
# HL7 FHIR (Fast Healthcare Interoperability Resources) R4 Exporter
import json
import datetime
import uuid


def generate_fhir_diagnostic_report(patient_token: str, accession_no: str,
                                    predicted_condition: str, confidence: float,
                                    recist_metrics: dict, clinician_name: str = "Dr. Sarah Mitchell") -> str:
    """
    Generate an authentic HL7 FHIR R4 DiagnosticReport resource JSON.
    Conforms to US Core Profile & IHE RAD TF standards for clinical radiology AI.
    """
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report_id = str(uuid.uuid4())
    obs_id = str(uuid.uuid4())

    snomed_codes = {
        "glioma": {"code": "44445000", "display": "Glioma of brain (disorder)"},
        "meningioma": {"code": "19483003", "display": "Meningioma of brain (disorder)"},
        "pituitary": {"code": "254956000", "display": "Pituitary adenoma (disorder)"},
        "notumor": {"code": "17621005", "display": "Normal brain imaging study (finding)"}
    }

    condition_code = snomed_codes.get(predicted_condition.lower(), {
        "code": "41641006", "display": "Intracranial neoplasm (disorder)"
    })

    fhir_bundle = {
        "resourceType": "DiagnosticReport",
        "id": report_id,
        "meta": {
            "profile": [
                "http://hl7.org/fhir/us/core/StructureDefinition/us-core-diagnosticreport-note"
            ],
            "lastUpdated": now
        },
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                        "code": "RAD",
                        "display": "Radiology"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "24627-2",
                    "display": "MRI Brain WO and W contrast"
                }
            ],
            "text": "Neuro-Oncology Diagnostic Brain MRI AI Report"
        },
        "subject": {
            "reference": f"Patient/{patient_token}",
            "display": f"Anonymized Patient {patient_token}"
        },
        "effectiveDateTime": now,
        "issued": now,
        "performer": [
            {
                "display": clinician_name,
                "type": "Practitioner"
            },
            {
                "display": "NeuroScan 2.5 AI Decision Support System",
                "type": "Device"
            }
        ],
        "imagingStudy": [
            {
                "identifier": {
                    "system": "urn:dicom:accession",
                    "value": accession_no
                }
            }
        ],
        "result": [
            {
                "reference": f"Observation/{obs_id}",
                "display": f"AI Impression: {condition_code['display']}"
            }
        ],
        "conclusionCode": [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": condition_code["code"],
                        "display": condition_code["display"]
                    }
                ]
            }
        ],
        "conclusion": (
            f"AI classification indicates {condition_code['display']} with {confidence:.1f}% confidence. "
            f"RECIST Staging: {recist_metrics.get('recist_category', 'N/A')}. "
            f"Tumor Volume: {recist_metrics.get('volume_cm3', 0.0)} cm³. "
            f"Mass Effect: {recist_metrics.get('mass_effect', 'None')}."
        ),
        "extension": [
            {
                "url": "https://neuroscan.ai/fhir/StructureDefinition/ai-confidence-score",
                "valueDecimal": round(confidence / 100.0, 4)
            },
            {
                "url": "https://neuroscan.ai/fhir/StructureDefinition/recist-volume-cm3",
                "valueDecimal": float(recist_metrics.get("volume_cm3", 0.0))
            },
            {
                "url": "https://neuroscan.ai/fhir/StructureDefinition/recist-max-diameter-mm",
                "valueDecimal": float(recist_metrics.get("max_diameter_mm", 0.0))
            }
        ]
    }

    return json.dumps(fhir_bundle, indent=2)
