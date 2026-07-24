# constrained_agent.py
import os
import time
from enum import Enum
from typing import Literal
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from tools import (
    assign_triage_level,
    check_hospital_resources,
    get_patient_history,
    assess_surgery_risk,
    check_transfer_options,
    allocate_resource,
)

load_dotenv()

class AllowedActions(str, Enum):
    ASSIGN_TRIAGE_LEVEL = "assign_triage_level"
    CHECK_RESOURCES = "check_hospital_resources"
    GET_PATIENT_HISTORY = "get_patient_history"
    ASSESS_SURGERY_RISK = "assess_surgery_risk"
    CHECK_TRANSFERS = "check_transfer_options"
    ALLOCATE_RESOURCE = "allocate_resource"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    FINAL_DECISION = "final_decision"

class ConstrainedAgentStep(BaseModel):
    thought: str = Field(description="Clinical reasoning and strategic planning for current step.")
    urgency_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(description="Patient urgency level.")
    action: AllowedActions = Field(description="Strictly allowed action to execute next.")
    action_input: dict = Field(default_factory=dict, description="Parameters required for selected action.")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.0)
structured_llm = llm.with_structured_output(ConstrainedAgentStep)

tools_map = {
    AllowedActions.ASSIGN_TRIAGE_LEVEL: assign_triage_level,
    AllowedActions.CHECK_RESOURCES: check_hospital_resources,
    AllowedActions.GET_PATIENT_HISTORY: get_patient_history,
    AllowedActions.ASSESS_SURGERY_RISK: assess_surgery_risk,
    AllowedActions.CHECK_TRANSFERS: check_transfer_options,
    AllowedActions.ALLOCATE_RESOURCE: allocate_resource,
}

SYSTEM_PROMPT = """You are a Constrained Hospital Emergency Triage AI Agent.
Strict Rules:
1. NEVER repeat an action that has already succeeded in the Execution History.
2. Complete the user request using the minimal necessary steps.
3. Once all required tasks (triage, history, resource check, or allocation) are completed, you MUST choose action='final_decision'.
4. Do not loop continuously. Move to 'final_decision' as soon as the core user instructions are fulfilled."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Execution History:\n{history}\n\nCurrent Task: {input}")
])

def run_constrained_agent(user_query: str, max_steps: int = 8):
    history = []
    print(f"\n[Task Started]: {user_query}\n" + "-" * 50)

    for step_num in range(1, max_steps + 1):
        history_text = "\n".join(history) if history else "None"
        formatted_prompt = prompt.format_messages(history=history_text, input=user_query)

        try:
            step_output = structured_llm.invoke(formatted_prompt)
        except Exception as e:
            print(f"API Error: {e}")
            break

        print(f"\n--- Step {step_num} ---")
        print(f"Thought: {step_output.thought}")
        print(f"Urgency: {step_output.urgency_level}")
        print(f"Action Chosen: {step_output.action.value}")

        if step_output.action == AllowedActions.FINAL_DECISION:
            print("\n[FINAL DECISION REACHED]")
            return step_output.thought

        if step_output.action == AllowedActions.ESCALATE_TO_HUMAN:
            print("\n[ESCALATED TO HUMAN DOCTOR]")
            return f"Escalated to doctor: {step_output.thought}"

        tool_func = tools_map.get(step_output.action)
        if tool_func:
            try:
                observation = tool_func(**step_output.action_input)
                print(f"Observation: {observation}")
                history.append(f"Action '{step_output.action.value}' succeeded with observation: {observation}")
            except Exception as e:
                error_msg = f"Action '{step_output.action.value}' failed with error: {str(e)}"
                print(f"Error Caught: {error_msg}")
                history.append(error_msg)

        time.sleep(1)

    return "Safety Timeout: Reached maximum allowed steps."

if __name__ == "__main__":
    case = "Patient P-102 has severe chest trauma. Assign triage level, check resources, and allocate ICU bed."
    result = run_constrained_agent(case)
    print(f"\nOutcome: {result}")