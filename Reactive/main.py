<<<<<<< HEAD
from rules import decide_patient
from testCases import get_example_patients

test_cases = get_example_patients()
passed = 0

for test in test_cases:
    result = decide_patient(**test["input"])

    print("-" * 30)
    print(test["id"])
    print("Expected:", test["expected"])
    print("Actual  :", result)

    if result == test["expected"]:
        print("PASS")
        passed += 1
    else:
        print("FAIL")

print("-" * 30)
=======
from rules import decide_patient
from testCases import get_example_patients

test_cases = get_example_patients()

passed = 0

for test in test_cases:
    result = decide_patient(**test["input"])

    print("-" * 30)
    print(test["name"])
    print("Expected:", test["expected"])
    print("Actual  :", result)

    if result == test["expected"]:
        print("PASS")
        passed += 1
    else:
        print("FAIL")

print("-" * 30)
>>>>>>> 68bb209bb74680a3757ce1748e0253e924ff7993
print(f"Passed {passed}/{len(test_cases)} Test Cases")