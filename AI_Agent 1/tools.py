# tools.py

def assign_triage_level(triage_level: str = "Level 1", patient_id: str = None, **kwargs):
    """Records the clinical triage severity level for the patient."""
    patient_info = f" for patient {patient_id}" if patient_id else ""
    return f"Patient triage level recorded as: Triage Level {triage_level}{patient_info}"

def check_hospital_resources(available_doctors: int = None, available_or_rooms: int = None, 
                             available_icu_beds: int = None, available_ventilators: int = None, **kwargs):
    """Checks current hospital bed and equipment availability based on current scenario."""
    # If the LLM passes context parameters, reflect them back accurately
    resources = {
        "doctors": available_doctors if available_doctors is not None else 2,
        "OR_rooms": available_or_rooms if available_or_rooms is not None else 1,
        "ICU_beds": available_icu_beds if available_icu_beds is not None else 1,
        "ventilators": available_ventilators if available_ventilators is not None else 1,
    }
    return f"Hospital Resource Status: {resources}"

def get_patient_history(patient_id: str = "P-102", **kwargs):
    """Retrieves patient medical history records."""
    return f"Patient {patient_id}: Record retrieved successfully."

def assess_surgery_risk(**kwargs):
    """Evaluates surgical intervention risk level."""
    return {"surgery_required": True, "risk_level": "HIGH"}

def check_transfer_options(**kwargs):
    """Checks transfer options to nearby medical facilities."""
    return "Nearest available hospital: City Central (12km away, ICU beds available)."

def allocate_resource(resource_type: str = "ICU_beds", **kwargs):
    """Allocates a specific medical resource or bed."""
    return f"Successfully allocated {resource_type} for the patient."
