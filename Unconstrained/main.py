from agent import agent_executor
from testCases import get_example_patients

test_cases = get_example_patients()

for test in test_cases:
    report = f"""
A patient case is provided below:
- Triage level: {test["input"]["triage_level"]}
- Age: {test["input"]["age"]}
- Needs surgery: {test["input"]["needs_surgery"]}
- Needs ventilator: {test["input"]["needs_ventilator"]}
- Internal bleeding: {test["input"]["internal_bleeding"]}
- Available doctors: {test["input"]["available_doctors"]}
- Available OR rooms: {test["input"]["available_or_rooms"]}
- Available ICU beds: {test["input"]["available_icu_beds"]}
- Available ventilators: {test["input"]["available_ventilators"]}

Your goal is to choose the best action for the patient.
Consider the patient's condition and available hospital resources.
Use the available tools whenever you need more information.

Choose one final decision from:
- IMMEDIATE_ICU
- IMMEDIATE_OR
- WAITLIST
- GENERAL_WARD
- STABILIZE_AND_MONITOR
- ESCALATE_TRANSFER

Return only the final decision.
"""

    result = agent_executor.invoke({"input": report})

    print(test["id"])
    print("Agent:", result["output"])
    print("-" * 30)