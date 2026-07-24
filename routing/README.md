# 🏥 Emergency Triage & Deterministic Resource Routing Agent

An enterprise-grade, deterministic routing system that combines **Pydantic data validation**, **Gemini Structured JSON Outputs**, and **Pure Python Execution Mapping** to automate patient triage and resource allocation in hospital emergency departments.

---

## 📌 Architecture Overview

+----------------------------+
                    |  Raw Patient & Hospital    |
                    |      Input Data (Dict)     |
                    +-------------+--------------+
                                  |
                                  v
                    +----------------------------+
                    |   PatientResourceInput     |
                    |     (Pydantic Validation)  |
                    +-------------+--------------+
                                  |
                                  v
                    +----------------------------+
                    |  Gemini Structured JSON    |
                    |         Classifier         |
                    +-------------+--------------+
                                  |
                                  v
                    +----------------------------+
                    |     RoutingDecision        |
                    |  (Route Enum + Reasoning)  |
                    +-------------+--------------+
                                  |
                                  v
                    +----------------------------+
                    |   ROUTE_HANDLER_MAP        |
                    | (Deterministic Python Exec)|
                    +-------------+--------------+
                                  |
                                  v
                    +----------------------------+
                    |   Final Execution Result   |
                    | (Status, Allocation, Task) |
                    +----------------------------+
---

## ⚙️ Classifier Logic & Decision Matrix

The core classifier maps patient severity (Triage Level 1–5) and real-time hospital resource constraints into **one of four strict pathways**:

| Allocation Route | Priority Level | Clinical & Resource Criteria | Assigned Hospital Action |
| :--- | :---: | :--- | :--- |
| **`DIRECT_OR_TRANSFER`** | `10 - 25` | Patient requires surgery (`needs_surgery=True`) AND OR rooms and doctors are available (`available_or_rooms > 0` & `available_doctors > 0`). | Dispatched immediately to Operating Room with surgical prep instructions. |
| **`DIRECT_ICU_ADMIT`** | `20 - 40` | Patient needs ICU or mechanical ventilation (no immediate surgery needed or OR unavailable) AND ICU beds are available (`available_icu_beds > 0`). | Admitted directly to ICU Bay; ventilator assigned if requested. |
| **`DEFERRED_HOLD_STABILIZE`** | `50 - 80` | Non-critical/urgent condition OR required resources are currently busy. Patient is stable enough to wait. | Placed in ER Holding Bay for IV fluids, monitoring, and re-evaluation every 15 min. |
| **`EXTERNAL_TRANSFER_ESCALATE`** | `1 - 10` | Critical state (Triage Level 1/2, active bleeding, pediatric severe emergency) where required local resources are **exhausted (0)**. | Immediate MedEvac / Critical Transport dispatch to a partner facility. |

---

## 🚀 Setup & Run

1. **Clone the repo** and install dependencies:

```bash
pip install -r requirements.txt
```

2. **Create your local `.env`** (do not commit this file):

```bash
copy .env.example .env
```

3. Open `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_real_key_here
```

4. **Run the benchmark suite:**

```bash
python run_test_cases.py
```

> Your real API key lives only in `.env`. That file is listed in `.gitignore` and will **not** be uploaded to GitHub.

---

## 📂 Component Map & Code Breakdown

The project is modularized into clear components:

```text
agent_project/
│
├── agent.py           # Enums, Pydantic Schemas, Gemini LLM Router, & Action Handlers
├── test_cases.py      # Patient Dataset Class & Test Suite Query Helpers
├── run_test_cases.py  # Benchmark Test Runner Script & Presentation Summary Generator
├── requirements.txt   # Python dependencies
├── .env.example       # Safe template for GEMINI_API_KEY (no real secret)
├── .gitignore         # Blocks .env and local junk from GitHub
└── README.md
```

================================================================================
RUNNING DETERMINISTIC ROUTING AGENT BENCHMARK SUITE
================================================================================

--------------------------------------------------------------------------------
Testing Patient [P-001]: Triage 1, Active Bleeding, Surgery Needed. OR available.
--------------------------------------------------------------------------------
-> Selected Route : DIRECT_OR_TRANSFER
-> Clinical Reason: Patient requires emergency surgery for active bleeding and OR resources are available.
-> Action Taken   : Dispatched immediately to Operating Room
-> Status         : APPROVED

================================================================================
FINAL TEST RESULTS SUMMARY
================================================================================
ID      | Assigned Route               | Status             | LLM Calls 
---------------------------------------------------------------------------
P-001   | DIRECT_OR_TRANSFER           | APPROVED           | 1         
P-002   | EXTERNAL_TRANSFER_ESCALATE   | ESCALATED_TRANSFER | 1         
P-003   | DIRECT_ICU_ADMIT             | APPROVED           | 1         
P-004   | DEFERRED_HOLD_STABILIZE      | QUEUED             | 1         
P-005   | DIRECT_ICU_ADMIT             | APPROVED           | 1         
P-006   | DIRECT_OR_TRANSFER           | APPROVED           | 1         
P-007   | DEFERRED_HOLD_STABILIZE      | QUEUED             | 1         
P-008   | EXTERNAL_TRANSFER_ESCALATE   | ESCALATED_TRANSFER | 1
