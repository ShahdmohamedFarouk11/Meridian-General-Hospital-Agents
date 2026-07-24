from typing import Dict, Any, List
from pydantic import BaseModel, Field


class PatientInput(BaseModel):
    triage_level: int = Field(description="1 (most critical) to 5 (least urgent)")
    age: int
    needs_surgery: bool
    needs_ventilator: bool
    internal_bleeding: bool
    available_doctors: int
    available_or_rooms: int
    available_icu_beds: int
    available_ventilators: int


class PatientTestCase(BaseModel):
    id: str
    description: str
    input: PatientInput


class PatientTestSuite:
    """Manages the benchmark test cases for Meridian General Hospital triage."""

    @staticmethod
    def get_all_patients() -> List[Dict[str, Any]]:
        """Returns raw dict format compatible with the agent runner."""
        return [
            {
                "id": "P-001",
                "description": "Triage 1, Active Bleeding, Surgery Needed. OR available.",
                "input": {
                    "triage_level": 1,
                    "age": 45,
                    "needs_surgery": True,
                    "needs_ventilator": False,
                    "internal_bleeding": True,
                    "available_doctors": 2,
                    "available_or_rooms": 1,
                    "available_icu_beds": 0,
                    "available_ventilators": 0,
                },
            },
            {
                "id": "P-002",
                "description": "Triage 1, Active Bleeding, Surgery Needed. OR capacity = 0.",
                "input": {
                    "triage_level": 1,
                    "age": 60,
                    "needs_surgery": True,
                    "needs_ventilator": False,
                    "internal_bleeding": True,
                    "available_doctors": 1,
                    "available_or_rooms": 0,
                    "available_icu_beds": 1,
                    "available_ventilators": 1,
                },
            },
            {
                "id": "P-003",
                "description": "Triage 2, Age 70, Stable. ICU bed required.",
                "input": {
                    "triage_level": 2,
                    "age": 70,
                    "needs_surgery": False,
                    "needs_ventilator": False,
                    "internal_bleeding": False,
                    "available_doctors": 3,
                    "available_or_rooms": 2,
                    "available_icu_beds": 2,
                    "available_ventilators": 0,
                },
            },
            {
                "id": "P-004",
                "description": "Triage 2, Stable, No Surgery. ICU beds = 0.",
                "input": {
                    "triage_level": 2,
                    "age": 55,
                    "needs_surgery": False,
                    "needs_ventilator": False,
                    "internal_bleeding": False,
                    "available_doctors": 2,
                    "available_or_rooms": 1,
                    "available_icu_beds": 0,
                    "available_ventilators": 2,
                },
            },
            {
                "id": "P-005",
                "description": "Triage 2, Ventilator Required. ICU Bed & Vent available.",
                "input": {
                    "triage_level": 2,
                    "age": 68,
                    "needs_surgery": False,
                    "needs_ventilator": True,
                    "internal_bleeding": False,
                    "available_doctors": 2,
                    "available_or_rooms": 1,
                    "available_icu_beds": 1,
                    "available_ventilators": 1,
                },
            },
            {
                "id": "P-006",
                "description": "Triage 1, Multi-resource need (Surgery + Vent). All available.",
                "input": {
                    "triage_level": 1,
                    "age": 60,
                    "needs_surgery": True,
                    "needs_ventilator": True,
                    "internal_bleeding": False,
                    "available_doctors": 1,
                    "available_or_rooms": 1,
                    "available_icu_beds": 1,
                    "available_ventilators": 1,
                },
            },
            {
                "id": "P-007",
                "description": "Triage 4, Non-urgent. All hospital resources = 0.",
                "input": {
                    "triage_level": 4,
                    "age": 30,
                    "needs_surgery": False,
                    "needs_ventilator": False,
                    "internal_bleeding": False,
                    "available_doctors": 0,
                    "available_or_rooms": 0,
                    "available_icu_beds": 0,
                    "available_ventilators": 0,
                },
            },
            {
                "id": "P-008",
                "description": "Triage 1, Pediatric emergency (Age 3), Surgery needed. OR = 0.",
                "input": {
                    "triage_level": 1,
                    "age": 3,
                    "needs_surgery": True,
                    "needs_ventilator": False,
                    "internal_bleeding": False,
                    "available_doctors": 1,
                    "available_or_rooms": 0,
                    "available_icu_beds": 1,
                    "available_ventilators": 1,
                },
            },
        ]

    @classmethod
    def get_by_id(cls, patient_id: str) -> Dict[str, Any]:
        """Fetch a single test patient by ID."""
        for patient in cls.get_all_patients():
            if patient["id"] == patient_id:
                return patient
        raise ValueError(f"Patient with ID '{patient_id}' not found.")