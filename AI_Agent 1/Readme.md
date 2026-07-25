# 🏥 Constrained ReAct Agent for Hospital Triage

## 📌 Overview

This project implements a **Constrained ReAct Agent** for emergency hospital triage.

It combines **LLM reasoning** with strict engineering constraints to produce safe, structured, and reliable medical decisions while preventing invalid actions and runtime failures.

---

## 🛡️ Core Engineering Guardrails

### ✅ Validation Schema
Uses **Pydantic** (`ConstrainedAgentStep`) to validate structured outputs and ensure only valid tool actions are generated.

### 🔒 Tool Allow-List
Limits execution to approved hospital tools only:

- `check_hospital_resources`
- `allocate_resource`
- `final_decision`

### ⏱️ Execution Budget
Limits reasoning to **6 maximum steps (`MAX_STEPS = 6`)** to avoid infinite loops and guarantee termination.

### ⚙️ Runtime Safety
Uses `**kwargs` in tool functions to safely handle dynamic parameters and prevent runtime parsing errors.

---

## 📂 Project Structure

```text
Constrained/
│
├── constrained_agent.py   # ReAct loop and constrained execution
├── tools.py               # Hospital tools
├── .env                   # API configuration
└── README.md              # Project documentation
```

---

## ✨ Features

- 🧠 Structured ReAct reasoning
- 🛡️ Schema validation with Pydantic
- 🔒 Restricted tool execution
- ⏱️ Limited reasoning steps
- ⚙️ Safe tool invocation
- 🏥 Hospital triage decision support
