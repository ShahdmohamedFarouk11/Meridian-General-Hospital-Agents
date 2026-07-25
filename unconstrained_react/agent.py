# 1) Imports
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent

from prompt import react_prompt

from tools import (
    check_hospital_resources,
    get_patient_history,
    assess_surgery_risk,
    check_transfer_options,
    allocate_resource
)

# 2) Load environment
load_dotenv()

# 3) Create Groq model
llm = ChatGroq(
   model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
).bind(stop=["\nObservation:", "\nObservation"])

# 4) Define tools
tools = [
    Tool(
        name="check_hospital_resources",
        func=check_hospital_resources,
        description=(
            "Check available hospital resources from raw resource data. "
            'Input must be JSON like: {"available_icu_beds": 1, "available_or_rooms": 0, '
            '"available_ventilators": 2, "available_doctors": 3}'
        ),
    ),
    Tool(
        name="get_patient_history",
        func=get_patient_history,
        description=(
            "Get a patient's medical history. "
            "Input must be the patient id only, exactly as given (e.g. P-001). "
            "Do not invent patient ids that were not mentioned in the question."
        ),
    ),
    Tool(
        name="assess_surgery_risk",
        func=assess_surgery_risk,
        description=(
            "Assess surgical risk for a patient. "
            'Input must be JSON like: {"internal_bleeding": true, "needs_surgery": true}'
        ),
    ),
    Tool(
        name="check_transfer_options",
        func=check_transfer_options,
        description="Check whether transferring the patient to another hospital is an option. Input can be empty.",
    ),
    Tool(
        name="allocate_resource",
        func=allocate_resource,
        description=(
            "Allocate a hospital resource only if available. "
            'Input must be JSON like: {"resource": "ICU bed", '
            '"available_resources": {"icu_beds": 1, "or_rooms": 0, "ventilators": 1}}. '
            'Valid "resource" values: "OR room", "ICU bed", "ventilator".'
        ),
    ),
]
 

# 5) Create ReAct Agent
agent = create_react_agent(
    llm,
    tools,
    react_prompt
)

# 6) Agent Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    handle_parsing_errors=True,
    early_stopping_method="force"
)