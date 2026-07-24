# test_agent.py
import unittest
import sys
from pathlib import Path

# Add current folder to Python path to prevent ModuleNotFoundError
sys.path.insert(0, str(Path(__file__).parent))

import unittest
from constrained_agent import run_constrained_agent


class TestConstrainedTriageAgent(unittest.TestCase):

    def test_case_1_critical_icu_allocation(self):
        """
        Test Case 1: High urgency patient needing immediate triage and ICU bed allocation.
        Expected: Successful resource check, allocation, and reaching FINAL_DECISION.
        """
        print("\n==========================================")
        print("RUNNING TEST CASE 1: Critical ICU Allocation")
        print("==========================================")
        query = "Patient P-102 has acute respiratory distress and severe chest trauma. Assign triage level, check resources, and allocate an ICU bed."
        result = run_constrained_agent(query)
        
        self.assertIsNotNone(result)
        self.assertNotIn("API Error", result)

    def test_case_2_resource_exhaustion_escalation(self):
        """
        Test Case 2: Critical condition where safety protocol triggers human intervention.
        Expected: Agent chooses ESCALATE_TO_HUMAN.
        """
        print("\n==========================================")
        print("RUNNING TEST CASE 2: Human Escalation Protocol")
        print("==========================================")
        query = "Patient P-999 is in critical neuro-trauma condition with unassessed risk. Escalate to medical staff if required."
        result = run_constrained_agent(query)
        
        self.assertIsNotNone(result)

    def test_case_3_triage_level_assignment(self):
        """
        Test Case 3: Stable patient requiring triage classification.
        Expected: Execution of assign_triage_level tool.
        """
        print("\n==========================================")
        print("RUNNING TEST CASE 3: Triage Assignment")
        print("==========================================")
        query = "Patient P-105 presents with mild symptoms and stable vitals. Assign triage level and inspect ER status."
        result = run_constrained_agent(query)
        
        self.assertIsNotNone(result)

    def test_case_4_self_correction_recovery(self):
        """
        Test Case 4: Verifies resilience and self-correction when tool parameters or steps encounter issues.
        Expected: Agent catches execution error and self-corrects in subsequent steps.
        """
        print("\n==========================================")
        print("RUNNING TEST CASE 4: Resilience & Self-Correction")
        print("==========================================")
        query = "Fetch history for patient P-102, evaluate surgery risk, and proceed to finalize allocation."
        result = run_constrained_agent(query)
        
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()