# 🏥 Unconstrained Agent
 
## 📌 Overview
This project implements the **Unconstrained Agent** approach for the Critical ICU & Operating Room Allocation problem.
Unlike rule-based agents, this agent reasons freely about each patient case using the available tools before making a decision, guided by lightweight decision hints in the prompt (rather than hard-coded rules).
 
---
 
## 🗂️ Project Structure
```
Unconstrained/
├── agent.py           # Agent setup: LLM, tools binding, AgentExecutor
├── tools.py            # Hospital tool functions (resources, risk, allocation...)
├── prompt.py           # ReAct prompt template with decision guidance rules
├── testCases.py        # Sample patient scenarios for testing
├── main.py             # Entry point — runs all test cases
├── requirements.txt     # Python dependencies
├── .env.example          # Template for required environment variables
└── .gitignore            # Excludes .env, .venv, and cache files from git
```
 
---
 
## 🔧 Setup & Installation
 
**1. Clone the repository**
```bash
git clone https://github.com/ShahdmohamedFarouk11/Meridian-General-Hospital-Agents.git
cd Meridian-General-Hospital-Agents/Unconstrained
```
 
**2. Create and activate a virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```
 
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
 
**4. Set up environment variables**
 
Copy `.env.example` to a new file named `.env`, then add your own Groq API key (from console.groq.com):
```
GROQ_API_KEY=your_actual_groq_api_key_here
```
 
**5. Run the agent**
```bash
python main.py
```
 
---
 
## 🎯 What I Implemented
- Built a ReAct agent using LangChain and Groq (`llama-3.3-70b-versatile`).
- Added 5 hospital tools:
  - `check_hospital_resources` — reports available ICU beds, OR rooms, ventilators, and doctors.
  - `get_patient_history` — retrieves a patient's medical history.
  - `assess_surgery_risk` — evaluates surgical risk based on patient condition.
  - `check_transfer_options` — checks whether transfer to another hospital is possible.
  - `allocate_resource` — allocates a specific resource if available.
- Designed a ReAct prompt (Thought → Action → Observation) with added decision guidance:
  - Choose `IMMEDIATE_ICU` only if the patient requires intensive care.
  - Otherwise choose `GENERAL_WARD` when the condition is stable.
  - Choose `WAITLIST` if immediate treatment is unavailable and the patient can safely wait.
- Tested the agent on 8 emergency scenarios covering varying triage levels, ages, and resource availability.
### 🩺 Possible Decisions
The agent selects one final decision per patient case from:
 
| Decision | Meaning |
|---|---|
| `IMMEDIATE_ICU` | Admit directly to ICU |
| `IMMEDIATE_OR` | Take to operating room immediately |
| `WAITLIST` | Add to the waiting list |
| `GENERAL_WARD` | Admit to a general ward |
| `STABILIZE_AND_MONITOR` | Stabilize and monitor patient |
| `ESCALATE_TRANSFER` | Escalate transfer to another hospital |
 
---
 
## ✅ Results
 
Latest run on all 8 test cases (`testCases.py`):
 
| Case | Triage | Needs Surgery | Internal Bleeding | Needs Ventilator | Agent Decision |
|---|---|---|---|---|---|
| P-001 | 1 | ✅ | ✅ | ❌ | `ESCALATE_TRANSFER` |
| P-002 | 1 | ✅ | ✅ | ❌ | `IMMEDIATE_ICU` |
| P-003 | 2 | ❌ | ❌ | ❌ | `GENERAL_WARD` |
| P-004 | 2 | ❌ | ❌ | ❌ | `GENERAL_WARD` |
| P-005 | 2 | ❌ | ❌ | ✅ | `IMMEDIATE_ICU` |
| P-006 | 1 | ✅ | ❌ | ✅ | `IMMEDIATE_OR` |
| P-007 | 4 | ❌ | ❌ | ❌ | `ESCALATE_TRANSFER` |
| P-008 | 1 | ✅ | ❌ | ❌ | `ESCALATE_TRANSFER` |
 
Compared to the previous prompt (without explicit decision rules), adding guidance for `IMMEDIATE_ICU` / `GENERAL_WARD` / `WAITLIST` made stable, low-acuity cases (P-003, P-004) noticeably more consistent — both now correctly resolve to `GENERAL_WARD` instead of unnecessarily occupying an ICU bed.
 
---
 
## ⚠️ Challenges
- **Inconsistent final decisions despite successful actions**: in P-001, the agent successfully allocated an OR room (`OR room allocated successfully`) but still chose `ESCALATE_TRANSFER` as the final answer, ignoring its own successful allocation.
- **New parsing errors**: `Invalid Format: Missing 'Action Input:' after 'Action:'` appeared in P-004 and P-005, caused by the agent outputting `Action: None` — a format the ReAct parser doesn't recognize.
- `get_patient_history` is non-functional: it expects an integer patient ID, but all test cases use string IDs (e.g. `P-001`), so the lookup always fails. The tool is never actually exercised by the test cases.
- Resource allocation is simulated in-memory and not persisted between runs.
- The "do not repeat the same tool with the same input" rule in the prompt is not enforced in code — it's just a written instruction the LLM can ignore.
---
 
## 🚀 Future Improvements
- Fix or remove the broken `get_patient_history` tool (mismatched ID format).
- Add stricter output validation to prevent `Action: None` / malformed actions from reaching the parser.
- Add dynamic hospital resources (e.g., connect to a live database instead of static test cases).
- Add an evaluation script that compares agent decisions against expected/ground-truth outcomes to measure accuracy.
- Add a final consistency check that re-validates the chosen decision against the tool observations already gathered (to catch cases like P-001).
---
 
## 🛠️ Technologies
- Python
- LangChain
- Groq LLM (`llama-3.3-70b-versatile`)
 
