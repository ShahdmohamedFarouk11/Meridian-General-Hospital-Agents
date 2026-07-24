# tools.py

def assign_triage_level(triage_level: str = "Level 1", patient_id: str = None, **kwargs):
    """Records the clinical triage severity level for the patient."""
    patient_info = f" for patient {patient_id}" if patient_id else ""
    return f"Patient triage level recorded as: {triage_level}{patient_info}"

def check_hospital_resources(**kwargs):
    """Checks current hospital bed and equipment availability."""
    return {"ICU_beds": 2, "ER_beds": 5, "ventilators": 1}

def get_patient_history(patient_id: str = "P-102", **kwargs):
    """Retrieves patient medical history records."""
    return f"Patient {patient_id}: Severe trauma, no known drug allergies, blood type O+."

def assess_surgery_risk(**kwargs):
    """Evaluates surgical intervention risk level."""
    return {"surgery_required": True, "risk_level": "HIGH"}

def check_transfer_options(**kwargs):
    """Checks transfer options to nearby medical facilities."""
    return "Nearest available hospital: City Central (12km away, 4 ICU beds)."

def allocate_resource(resource_type: str = "ICU_beds", **kwargs):
    """Allocates a specific medical resource or bed."""
    return f"Successfully allocated {resource_type} for the patient."