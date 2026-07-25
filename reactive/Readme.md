# 🏥 Reactive Agent (Rule-Based)
 
## 📌 Overview
This project implements a **Reactive (Rule-Based) Agent** for the Critical ICU & Operating Room Allocation problem.
Unlike the Unconstrained (LLM-based) agent, this agent makes decisions using a fixed set of hand-written `if/else` rules — no LLM calls, no tools, fully deterministic. Given the same input, it always produces the same output.
 
---
 
## 🗂️ Project Structure
```
Reactive/
├── rules.py           # decide_patient(): the full rule-based decision logic
├── testCases.py        # Sample patient scenarios with expected outcomes
├── main.py             # Entry point — runs all test cases and checks PASS/FAIL
└── requirements.txt     # Python dependencies (if any external packages are used)
```
 
---
 
## 🔧 Setup & Installation
 
**1. Clone the repository**
```bash
git clone https://github.com/ShahdmohamedFarouk11/Meridian-General-Hospital-Agents.git
cd Meridian-General-Hospital-Agents/Reactive
```
 
**2. Run the agent**
No API key or environment setup needed — this agent is pure Python logic with no external dependencies.
```bash
python main.py
```
 
---
 
## 🎯 What I Implemented
- Built `decide_patient()` — a deterministic function that takes patient and hospital-resource data and returns one final decision.
- Encoded ~14 prioritized rules covering:
  - Triage level 1 cases needing a ventilator, surgery, or with internal bleeding.
  - General internal bleeding + surgery combinations regardless of triage.
  - Resource shortages (no OR rooms, no ICU beds) with age-based escalation for very young/old patients.
  - Triage level 2 and 3 cases (surgery, ventilator, internal bleeding).
  - Fallback rules for triage 4+ and any unmatched case → `GENERAL_WARD`.
- Added a test harness (`main.py`) that runs 8 test cases against expected outcomes and reports PASS/FAIL per case, with a simple accuracy check.
### 🩺 Possible Decisions
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
 
Latest run on all 8 test cases (`testCases.py`): **6/8 PASS (75%)**
 
| Case | Triage | Needs Surgery | Needs Ventilator | Internal Bleeding | Expected | Actual | Result |
|---|---|---|---|---|---|---|---|
| P-001 | 1 | ✅ | ❌ | ✅ | `IMMEDIATE_OR` | `IMMEDIATE_OR` | ✅ PASS |
| P-002 | 1 | ✅ | ❌ | ✅ | `WAITLIST` | `WAITLIST` | ✅ PASS |
| P-003 | 2 | ❌ | ❌ | ❌ | `GENERAL_WARD` | `GENERAL_WARD` | ✅ PASS |
| P-004 | 2 | ❌ | ❌ | ❌ | `GENERAL_WARD` | `GENERAL_WARD` | ✅ PASS |
| P-005 | 2 | ❌ | ✅ | ❌ | `IMMEDIATE_ICU` | `IMMEDIATE_ICU` | ✅ PASS |
| P-006 | 1 | ✅ | ✅ | ❌ | `IMMEDIATE_OR` | `IMMEDIATE_ICU` | ❌ FAIL |
| P-007 | 4 | ❌ | ❌ | ❌ | `GENERAL_WARD` | `GENERAL_WARD` | ✅ PASS |
| P-008 | 1 (age 3) | ✅ | ❌ | ❌ | `ESCALATE_TRANSFER` | `WAITLIST` | ❌ FAIL |
 
Unlike the Unconstrained agent, results here are **100% reproducible** across runs — the same input always yields the same output, since there is no LLM involved.
 
---
 
## ⚠️ Challenges / Known Bugs
 
**1. P-006 — Rule ordering conflict (ventilator vs. surgery priority)**
Rule 1 checks `needs_ventilator` before Rule 2 checks `needs_surgery`. For a triage-1 patient who needs *both* surgery and a ventilator, Rule 1 fires first and returns `IMMEDIATE_ICU`, even though surgery should take priority (expected `IMMEDIATE_OR`). The rule order doesn't reflect the intended clinical priority.
 
**2. P-008 — Age-based escalation rule is unreachable for triage-1 patients**
Rule 5 is meant to escalate very young (<5) or elderly (>65) patients to `ESCALATE_TRANSFER` when no OR room is available. However, Rule 2 (triage-1 + needs_surgery) already returns `WAITLIST` before execution ever reaches Rule 5 — so the age check never applies to triage-1 cases, only to lower-priority triage levels.
 
**3. General maintainability risk**
With 14 sequential `if/return` rules, the order matters a lot, and it's easy to introduce this kind of shadowing bug when adding new rules. There's no explicit priority ranking documented in the code, making it hard to reason about which rule should win when multiple conditions overlap.
 
---
 
## 🚀 Future Improvements
- Reorder Rule 1 and Rule 2 (or merge them) so that `needs_surgery` takes priority over `needs_ventilator` at triage level 1, fixing P-006.
- Move the age-based escalation check (Rule 5) earlier, or merge it into Rule 2, so it also applies to triage-1 patients — fixing P-008.
- Add inline comments documenting the *intended* priority order of rules, to make future edits safer.
- Add more test cases covering edge combinations (e.g., surgery + ventilator + internal bleeding together) to catch similar ordering conflicts before they reach production.
- Consider refactoring into a priority-scored rule table instead of sequential if/return, to make rule precedence explicit and easier to test.
---
 
## 🛠️ Technologies
- Python (pure logic, no external ML/LLM dependencies)
 
