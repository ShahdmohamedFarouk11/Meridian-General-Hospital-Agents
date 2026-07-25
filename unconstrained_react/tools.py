from datetime import datetime
import ast


# Tool 1
def check_hospital_resources(data):

    if isinstance(data, str):

        if data.startswith("data ="):
            data = data.split("=", 1)[1].strip()

        data = ast.literal_eval(data)

    return {
        "icu_beds": data.get("available_icu_beds", 0),
        "or_rooms": data.get("available_or_rooms", 0),
        "ventilators": data.get("available_ventilators", 0),
        "available_doctors": data.get("available_doctors", 0)
    }


# Tool 2
def get_patient_history(patient_id):

    try:
        patient_id = int(patient_id)
    except:
        return "Patient history not available"

    patients = {
        1: {
            "age": 4,
            "heart_disease": True,
            "previous_operations": 2,
            "allergies": ["penicillin"]
        },

        2: {
            "age": 35,
            "heart_disease": False,
            "previous_operations": 0,
            "allergies": []
        }
    }

    return patients.get(patient_id, "Patient not found")


# Tool 3
def assess_surgery_risk(data):

    if isinstance(data, str):

        if data.startswith("data ="):
            data = data.split("=", 1)[1].strip()

        data = ast.literal_eval(data)

    internal_bleeding = data.get("internal_bleeding", False)
    needs_surgery = data.get("needs_surgery", False)

    risk = "LOW"

    if internal_bleeding and needs_surgery:
        risk = "HIGH"

    return {
        "risk_level": risk,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


# Tool 4
def check_transfer_options(_=None):

    return {
        "available": True
    }


# Tool 5
def allocate_resource(data):

    if isinstance(data, str):

        if data.startswith("data ="):
            data = data.split("=", 1)[1].strip()

        try:
            data = ast.literal_eval(data)

        except:
            return "Invalid allocation request"

    resource = data.get("resource")
    available = data.get("available_resources", {})

    if resource == "OR room":

        if available.get("or_rooms", 0) <= 0:
            return "Cannot allocate OR room: no rooms available"

    elif resource == "ICU bed":

        if available.get("icu_beds", 0) <= 0:
            return "Cannot allocate ICU bed: no beds available"

    elif resource == "ventilator":

        if available.get("ventilators", 0) <= 0:
            return "Cannot allocate ventilator: none available"

    return f"{resource} allocated successfully"