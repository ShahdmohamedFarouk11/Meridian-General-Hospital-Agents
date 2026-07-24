# Meridian-General-Hospital-Agents
# Constrained ReAct Agent for Hospital Triage
This directory contains the implementation of the **Constrained ReAct Architecture** for Emergency Hospital Triage. It combines LLM-driven multi-step reasoning with strict engineering guardrails to prevent schema hallucinations, handle runtime parameter mismatches, and enforce safety in critical care workflows.
##  Core Engineering Guardrails
The guardrails are explicitly defined in the codebase:
1. **Validation Schema (`ConstrainedAgentStep`)**: Built using `Pydantic` to enforce structured JSON output. Tool actions are restricted strictly to an explicit `Enum` (`AllowedActions`) to eliminate hallucinated tool names.
2. **Tool Allow-List (`tools_map`)**: Limits dynamic execution strictly to authorized triage functions (`check_hospital_resources`, `assess_surgery_risk`, `allocate_resource`, etc.).
3. **Execution Budget (`MAX_STEPS = 6`)**: Enforces a strict upper bound of 6 steps to guarantee fast termination or automatic human escalation.
4. **Error Feedback & Resilience Loop**: Captures runtime exceptions (e.g., unexpected keyword arguments) into the interaction history, allowing the agent to self-correct in subsequent steps without crashing
##  File Structure
* `constrained_agent.py`: Main agent runtime with custom ReAct loop, Groq Llama-3.3-70B model initialization, and Pydantic schema parsing.
* `tools.py`: Emergency hospital tool implementations.
* `.env.example`: Template for environment variable setup.
* `README.md`: System documentation and execution guidelines.
