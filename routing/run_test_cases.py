import time

from agent import run_routing_agent
from test_cases import PatientTestSuite


def run_benchmark_tests():
    print("=" * 80)
    print("RUNNING DETERMINISTIC ROUTING AGENT BENCHMARK SUITE")
    print("=" * 80)

    # Calling test suite class
    patients = PatientTestSuite.get_all_patients()
    results = []

    for i, patient in enumerate(patients):
        p_id = patient["id"]
        p_desc = patient.get("description", "")
        p_input = patient["input"]

        print(f"\n--------------------------------------------------------------------------------")
        print(f"Testing Patient [{p_id}]: {p_desc}")
        print(f"--------------------------------------------------------------------------------")

        # Call the routing agent (pause between calls to stay under free-tier rate limits)
        if i > 0:
            time.sleep(14)
        result = run_routing_agent(p_id, p_input)
        results.append(result)

        print(f"-> Selected Route : {result['route_selected']}")
        print(f"-> Clinical Reason: {result['reasoning']}")
        print(f"-> Action Taken   : {result['execution_output']['action_taken']}")
        print(f"-> Status         : {result['execution_output']['status']}")

    # Print clean summary table
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS SUMMARY (FOR README / PRESENTATION)")
    print("=" * 80)
    print(f"{'ID':<7} | {'Assigned Route':<28} | {'Status':<18} | {'LLM Calls':<10}")
    print("-" * 75)
    for r in results:
        print(
            f"{r['patient_id']:<7} | "
            f"{r['route_selected']:<28} | "
            f"{r['execution_output']['status']:<18} | "
            f"{r['llm_calls']:<10}"
        )


if __name__ == "__main__":
    run_benchmark_tests()