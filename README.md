# 🏥 Meridian General Hospital Agents

## 🏥 The Company

**Meridian General Hospital** is a fictional hospital created for this project to simulate emergency patient triage and hospital resource management.

The hospital receives patients with different medical conditions while operating with limited resources such as operating rooms, ICU beds, ventilators, and available doctors. During busy periods, making the right decision quickly is just as important as making the right decision accurately.

---

## ❗ The Problem

The goal of this project is to determine the most appropriate routing decision for each patient based on both the patient's clinical condition and the hospital's current resource availability.

For every patient, the system recommends one of the following actions:

- Send the patient to the Operating Room (OR)
- Admit the patient to the ICU
- Transfer the patient to another hospital
- Delay treatment until resources become available
- Escalate the case for manual review

Each decision considers multiple factors, including:

- Triage level
- Patient age
- Surgery requirement
- Ventilator requirement
- ICU bed availability
- Operating room availability
- Doctor availability
- Transfer availability

To make the evaluation more realistic, we created both standard and challenging patient scenarios, including unusual combinations of medical conditions and resource limitations that may occur in real emergency departments.

---

## 🤖 Why This Needs an Agent Instead of a Simple Script

At first, a rule-based solution seemed sufficient for this problem. However, as more patient conditions and hospital constraints were introduced, maintaining a fixed decision tree became increasingly difficult.

Different patients require multiple factors to be considered simultaneously, and small changes in rule ordering can produce incorrect or inconsistent decisions.

To better understand how different AI approaches handle this challenge, we implemented four independent solutions that solve the same hospital triage problem using different architectures.

Rather than focusing on a single implementation, this project compares deterministic rules, unconstrained reasoning, constrained reasoning, and structured routing to evaluate the trade-offs between flexibility, reliability, safety, and consistency when supporting emergency triage decisions.
 
## 🧩 The Four Implementations
 
| Folder | Approach | Model/Provider Expected |
|---|---|---|
| `reactive/` | Pure `if/else` decision function — zero LLM calls | None (pure Python) |
| `unconstrained_react/` | Free-reasoning ReAct agent with 5 tools, no output schema, no tool allow-list | Groq (`llama-3.3-70b-versatile`) |
| `constrained_react/` | ReAct agent with Pydantic-validated steps, a strict tool allow-list, and a hard `MAX_STEPS` budget | Groq (`llama-3.3-70b-versatile`) — *confirm and update if different* |
| `routing/` | Pydantic-validated input → single structured LLM classification call → deterministic Python routing map | Google Gemini (Structured JSON Outputs) |
 
**Each folder is runnable independently** — see the "How to Run" note inside each folder's own README (setup, dependencies, required environment variable) before running the comparison below.
 
---
 
## 📊 Comparison

| Metric | `reactive/` | `unconstrained_react/` | `constrained_react/` | `routing/` |
|---|---|---|---|---|
| **LLM calls per request** | 0 | Usually 3–6 tool/reasoning steps | Up to 6 steps (`MAX_STEPS = 6`) | Exactly 1 |
| **Token usage** | None | Relatively high due to multi-step reasoning | Moderate (limited by validation and step budget) | Low (single structured response) |
| **Latency** | Almost instant | Highest among the four approaches | Lower than the unconstrained agent | Low, since it makes only one LLM call |
| **Behavior on tricky inputs** | Missed some rule combinations (e.g., surgery + ventilator, pediatric surgery with no OR) | Occasionally produced inconsistent reasoning or parser errors | More robust thanks to schema validation and restricted tools, but still needs broader stress testing | Performed consistently on the tested cases, though additional edge-case evaluation is still recommended |
 
> ⚠️ **The comparison is based on the current implementation and representative test runs. Future work includes collecting detailed latency and token statistics across a larger benchmark set.**.
 
---
 
## 🔑 Key Takeaways
- A rules-only system is fast and free but brittle at rule intersections — bugs are logic errors, not randomness, which makes them fixable but also easy to miss until the wrong combination shows up.
- An unconstrained LLM agent can reason past the specific rules a script would need, but without validation it can also ignore its own evidence and produce an inconsistent final answer.
- Constraining the agent (schema validation, tool allow-list, step budget) is our hypothesis for closing that gap — this project's core open question is whether it actually does, which we still need to verify with real edge-case tests.
- Reducing LLM involvement to a single structured classification call (`routing/`) trades flexibility for predictability and lower cost — worth comparing directly once its latency/token numbers are in.
---
 
## 🚀 Next Steps (before final submission)
1. Rename folders to exactly: `reactive/`, `unconstrained_react/`, `routing/`, `constrained_react/`.
2. In `constrained_react/`, make sure the **validation schema**, **tool allow-list**, and **`MAX_STEPS` constant** are defined near the top of the main file with clear comments — not nested inside functions.
3. Run all four agents against the same 8 baseline cases **plus** 2–3 new "tricky" cases (e.g. all resources at 0 and transfer unavailable; a patient record missing a field; a 1-year-old needing both surgery and a ventilator).
4. Add real latency measurements (wrap each `invoke()`/API call with `time.time()`) and real token counts (from each provider's response metadata) to the comparison table above.
5. Confirm commit history reflects real, roughly-even contribution from all three team members across the four builds and the presentation (no one should be "presentation-only" or own more than two folders).
---
 
## 📁 Repository Structure
```
Meridian-Health-Systems-Agents/
├── reactive/                # Rule-based deterministic agent
├── unconstrained_react/     # Free-reasoning ReAct agent (Groq)
├── constrained_react/       # ReAct agent + Pydantic validation + tool allow-list + MAX_STEPS
├── routing/                 # Gemini structured classification + deterministic routing map
└── README.md                # This file
```
 
## 🛠️ Technologies Used Across the Project
- Python
- LangChain
- Groq LLM (`llama-3.3-70b-versatile`)
- Google Gemini (Structured JSON Outputs)
- Pydantic
