# neuro_copilot.py
# NeuroCopilot(TM) AI Surgical Resectability, Molecular Biomarker & Risk Engine
import numpy as np
import plotly.graph_objects as go


def calculate_surgical_risk(tumor_class: str, volume_cm3: float,
                            eloquent_proximity: str = "Adjacent (Within 5mm)",
                            vascular_encasement: bool = False,
                            patient_age: int = 54,
                            preop_kps: int = 80) -> dict:
    """
    Compute neurosurgical resectability index, Karnofsky Performance Status (KPS)
    trajectory, and WHO CNS tumor grade based on clinical imaging parameters.
    """
    # 1. WHO Staging & Grading Estimation
    who_grades = {
        "glioma": {
            "grade": "WHO Grade III / IV (High-Grade Infiltrative)",
            "histology": "Glioblastoma / Anaplastic Astrocytoma",
            "molecular_markers": ["IDH1/2 Mutation", "MGMT Methylation", "1p/19q Co-deletion", "TERT Promoter"],
            "chemo_regimen": "Temozolomide (Stupp Protocol) + Lomustine"
        },
        "meningioma": {
            "grade": "WHO Grade I / II (Extra-Axial Dural Mass)",
            "histology": "Meningothelial / Atypical Meningioma",
            "molecular_markers": ["NF2 Mutation", "TERT Promoter", "TRAF7", "AKT1"],
            "chemo_regimen": "Surgical Excision +/- Adjuvant Stereotactic Radiosurgery (CyberKnife)"
        },
        "pituitary": {
            "grade": "WHO Grade I (Benign Sellar / Suprasellar Neoplasm)",
            "histology": "Pituitary Neuroendocrine Tumor (PitNET)",
            "molecular_markers": ["Prolactin", "GH (Growth Hormone)", "ACTH / Corticotroph", "USP8"],
            "chemo_regimen": "Dopamine Agonists (Cabergoline) or Transsphenoidal Endoscopic Resection"
        },
        "notumor": {
            "grade": "Physiologic Normal Brain (No Neoplasm)",
            "histology": "Normal cortical and subcortical tissue",
            "molecular_markers": ["N/A"],
            "chemo_regimen": "None indicated"
        }
    }

    info = who_grades.get(tumor_class.lower(), who_grades["glioma"])

    if tumor_class.lower() == "notumor":
        return {
            "who_grade": info["grade"],
            "histology": info["histology"],
            "resectability_pct": 100.0,
            "resectability_class": "No Resection Required (Normal Study)",
            "molecular_markers": info["molecular_markers"],
            "chemo_regimen": info["chemo_regimen"],
            "projected_postop_kps": 100,
            "risk_scores": {"Eloquence": 0, "Mass Effect": 0, "Vascular": 0, "Depth": 0, "Edema": 0}
        }

    # 2. Risk scoring components (0 to 10 scale)
    eloquence_score = 9 if "Directly Involves" in eloquent_proximity else (6 if "Adjacent" in eloquent_proximity else 2)
    mass_score = min(10, int(volume_cm3 / 3.0))
    vascular_score = 8 if vascular_encasement else 2
    depth_score = 7 if tumor_class == "pituitary" or volume_cm3 > 18 else 4
    edema_score = 8 if tumor_class == "glioma" else 3

    # Resectability percentage formula (Gross Total Resection Feasibility)
    total_penalty = (eloquence_score * 3.5) + (mass_score * 2.0) + (vascular_score * 2.5) + (depth_score * 1.5)
    resectability_pct = max(15.0, min(95.0, round(100.0 - (total_penalty * 0.7), 1)))

    if resectability_pct >= 75.0:
        resectability_class = "High Feasibility for Gross Total Resection (GTR)"
    elif resectability_pct >= 45.0:
        resectability_class = "Subtotal Resection (STR) + Adjuvant Radiotherapy Indicated"
    else:
        resectability_class = "Biopsy Only / Stereotactic Radiosurgery (High Eloquent Risk)"

    # Projected Post-Op KPS (Functional status)
    kps_impact = int((eloquence_score + vascular_score) * 1.2)
    projected_postop_kps = max(30, min(100, preop_kps - kps_impact + 5))

    return {
        "who_grade": info["grade"],
        "histology": info["histology"],
        "resectability_pct": resectability_pct,
        "resectability_class": resectability_class,
        "molecular_markers": info["molecular_markers"],
        "chemo_regimen": info["chemo_regimen"],
        "projected_postop_kps": projected_postop_kps,
        "risk_scores": {
            "Eloquence Risk": eloquence_score,
            "Mass Effect": mass_score,
            "Vascular Infiltration": vascular_score,
            "Surgical Depth": depth_score,
            "Peritumoral Edema": edema_score
        }
    }


def render_risk_radar(risk_dict: dict) -> go.Figure:
    """
    Render a clinical multi-axis surgical risk radar chart.
    """
    categories = list(risk_dict.keys())
    values = list(risk_dict.values())
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(94, 83, 115, 0.35)',
        line=dict(color='#DBD8E3', width=2.5),
        name='Surgical Complexity Index'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(color='#a59cb8', size=9),
                gridcolor='rgba(219, 216, 227, 0.15)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#DBD8E3', size=11, family="Plus Jakarta Sans"),
                gridcolor='rgba(219, 216, 227, 0.15)'
            ),
            bgcolor='rgba(42, 37, 57, 0.9)'
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        height=320,
        margin=dict(l=40, r=40, t=30, b=30),
        showlegend=False
    )

    return fig


def render_survival_trajectory(tumor_class: str, resectability_pct: float) -> go.Figure:
    """
    Render projected 24-month progression-free survival probability curves comparing
    different intervention strategies (Surgery + Stupp vs Biopsy vs Observation).
    """
    months = np.array([0, 3, 6, 9, 12, 15, 18, 21, 24])

    if tumor_class.lower() == "glioma":
        # Glioblastoma survival decay
        gtr_curve = 100 * np.exp(-0.038 * months) * (resectability_pct / 100.0) + (100 - resectability_pct) * 0.45 * np.exp(-0.07 * months)
        str_curve = 100 * np.exp(-0.072 * months)
        biopsy_curve = 100 * np.exp(-0.11 * months)
    elif tumor_class.lower() == "meningioma":
        # Benign high progression-free survival
        gtr_curve = 100 * np.exp(-0.004 * months)
        str_curve = 100 * np.exp(-0.015 * months)
        biopsy_curve = 100 * np.exp(-0.035 * months)
    else:
        # Pituitary adenoma
        gtr_curve = 100 * np.exp(-0.003 * months)
        str_curve = 100 * np.exp(-0.012 * months)
        biopsy_curve = 100 * np.exp(-0.025 * months)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=gtr_curve, mode='lines+markers', name='Gross Total Resection (GTR) + Adjuvant',
        line=dict(color='#10b981', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=months, y=str_curve, mode='lines+markers', name='Subtotal Resection (STR) + Radiotherapy',
        line=dict(color='#38bdf8', width=2.5, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=months, y=biopsy_curve, mode='lines', name='Stereotactic Biopsy Only',
        line=dict(color='#ef4444', width=2, dash='dot')
    ))

    fig.update_layout(
        title="Projected 24-Month Progression-Free Survival (Kaplan-Meier Simulation)",
        xaxis_title="Months Post-Intervention",
        yaxis_title="Progression-Free Probability (%)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#cbd5e1"),
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)"),
        yaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)", range=[0, 105]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig
