import json
import os
import time
from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ==========================================
# 1. ENUMS & SCHEMAS FOR ROUTING
# ==========================================

class AllocationRoute(str, Enum):
    DIRECT_OR_TRANSFER = "DIRECT_OR_TRANSFER"
    DIRECT_ICU_ADMIT = "DIRECT_ICU_ADMIT"
    DEFERRED_HOLD_STABILIZE = "DEFERRED_HOLD_STABILIZE"
    EXTERNAL_TRANSFER_ESCALATE = "EXTERNAL_TRANSFER_ESCALATE"


class PatientResourceInput(BaseModel):
    triage_level: int = Field(description="1 (most critical) to 5 (least urgent)")
    age: int
    needs_surgery: bool
    needs_ventilator: bool
    internal_bleeding: bool
    available_doctors: int
    available_or_rooms: int
    available_icu_beds: int
    available_ventilators: int


class RoutingDecision(BaseModel):
    route: AllocationRoute = Field(description="The assigned route based on clinical priorities and resource availability.")
    reasoning: str = Field(description="A concise 1-2 sentence clinical justification for this route assignment.")
    priority_score: int = Field(description="Priority score from 1 (highest urgency) to 100 (lowest)")


# ==========================================
# 2. DETERMINISTIC EXECUTION HANDLERS
# ==========================================

def execute_direct_or_transfer(patient: PatientResourceInput) -> Dict[str, Any]:
    return {
        "status": "APPROVED",
        "action_taken": "Dispatched immediately to Operating Room",
        "resources_allocated": {
            "or_room": 1,
            "doctors_assigned": 2 if patient.internal_bleeding else 1,
            "icu_reserved": patient.needs_ventilator or patient.triage_level == 1
        },
        "instructions": "Prepare patient for emergency surgical intervention."
    }

def execute_direct_icu_admit(patient: PatientResourceInput) -> Dict[str, Any]:
    return {
        "status": "APPROVED",
        "action_taken": "Admitted directly to ICU Bay",
        "resources_allocated": {
            "icu_bed": 1,
            "ventilator": 1 if patient.needs_ventilator else 0
        },
        "instructions": "Initiate continuous ICU monitoring and mechanical ventilation if required."
    }

def execute_deferred_hold_stabilize(patient: PatientResourceInput) -> Dict[str, Any]:
    return {
        "status": "QUEUED",
        "action_taken": "Placed in ER Holding Bay for Stabilization",
        "resources_allocated": {"holding_bed": 1, "monitoring": "Vitals Bay"},
        "instructions": "Administer IV fluids/support. Re-evaluate resource availability every 15 minutes."
    }

def execute_external_transfer_escalate(patient: PatientResourceInput) -> Dict[str, Any]:
    return {
        "status": "ESCALATED_TRANSFER",
        "action_taken": "Initiated Emergency Medical Transfer to Partner Facility",
        "resources_allocated": {"transport_unit": "MedEvac / Critical Transport"},
        "instructions": "Critical resource shortfall. Stabilize patient for immediate transit."
    }


ROUTE_HANDLER_MAP = {
    AllocationRoute.DIRECT_OR_TRANSFER: execute_direct_or_transfer,
    AllocationRoute.DIRECT_ICU_ADMIT: execute_direct_icu_admit,
    AllocationRoute.DEFERRED_HOLD_STABILIZE: execute_deferred_hold_stabilize,
    AllocationRoute.EXTERNAL_TRANSFER_ESCALATE: execute_external_transfer_escalate,
}


# ==========================================
# 3. ROUTING AGENT CORE LOGIC
# ==========================================

def run_routing_agent(patient_id: str, raw_input: Dict[str, Any]) -> Dict[str, Any]:
    """Processes patient data with 1 LLM call and executes pure Python action logic."""
    patient_model = PatientResourceInput(**raw_input)

    system_prompt = (
        "You are the Emergency Triage & Resource Routing Classifier for Meridian General Hospital.\n"
        "Analyze the patient clinical state and current hospital resource constraints.\n"
        "Assign the patient to EXACTLY ONE of these categories:\n"
        "1. DIRECT_OR_TRANSFER: Patient requires surgery, AND OR rooms and doctors are available (>0).\n"
        "2. DIRECT_ICU_ADMIT: Patient needs ICU/Ventilator (no immediate OR needed/available), AND ICU beds are available (>0).\n"
        "3. DEFERRED_HOLD_STABILIZE: Patient has urgent/non-critical triage or stable need, but required direct resources are currently busy. Place on ER hold.\n"
        "4. EXTERNAL_TRANSFER_ESCALATE: Critical condition (Triage 1/2 or active bleeding/pediatric emergency) where required resources (OR/ICU/Doctors) are 0/exhausted, necessitating immediate external hospital transfer.\n"
    )

    user_prompt = f"PATIENT_ID: {patient_id}\nDATA:\n{json.dumps(patient_model.model_dump(), indent=2)}"

    response = None
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=f"{system_prompt}\n\n{user_prompt}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RoutingDecision,
                    temperature=0.0,
                ),
            )
            break
        except (genai_errors.ClientError, genai_errors.ServerError) as exc:
            if attempt == 4:
                raise
            wait_s = 15 * (attempt + 1)
            print(f"   (API busy/rate-limited, retrying in {wait_s}s...)")
            time.sleep(wait_s)

    decision = RoutingDecision.model_validate_json(response.text)
    handler_fn = ROUTE_HANDLER_MAP[decision.route]
    execution_result = handler_fn(patient_model)

    return {
        "patient_id": patient_id,
        "llm_calls": 1,
        "route_selected": decision.route.value,
        "reasoning": decision.reasoning,
        "priority_score": decision.priority_score,
        "execution_output": execution_result
    }