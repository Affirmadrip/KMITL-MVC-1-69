from controller import ContestController
from views import ResultView

SEED_PATH = "seed_data.json"


def run_case(case_id: str, action: str, outcome: dict, expected_hint: str):
    status = "PASS" if outcome["success"] else "FAIL(rejected)"
    print(f"[{case_id}] {action}")
    print(f"   Actual   : {status} - {outcome['message']}")
    print(f"   Expected : {expected_hint}")
    print()


def main():
    controller = ContestController.load_from_seed(SEED_PATH)

    print("=== State before T1 (after loading seed_data.json) ===")
    for c in controller.list_contestants():
        print(f"  {c.contestant_id} {c.name:<20} Status: {c.status} "
              f"(votes {len(c.decisions)}/4, GB by: {c.golden_buzzer_by})")
    print()

    outcome = controller.submit_decision("J02", "P01", "PASS")
    run_case("T1", "J02 gives PASS to P01", outcome, "Recorded successfully")

    outcome = controller.submit_decision("J01", "P01", "PASS")
    run_case("T2", "J01 tries to give a decision to P01 again", outcome,
              "Rejected because J01 already judged P01")

    outcome = controller.submit_decision("J04", "P02", "PASS")
    run_case("T3", "J04 gives PASS to P02", outcome,
              "4th vote received; P02 has 3 PASS / 1 FAIL and status becomes PASSED")

    outcome = controller.use_golden_buzzer("J02", "P03")
    run_case("T4", "J02 uses Golden Buzzer on P03", outcome,
              "P03 advances immediately and J02 has used their Golden Buzzer")

    outcome = controller.use_golden_buzzer("J04", "P04")
    run_case("T5", "J04 tries to use Golden Buzzer on P04", outcome,
              "Rejected because J04 already used Golden Buzzer in the seed data")

    outcome = controller.submit_decision("J04", "P05", "FAIL")
    run_case("T6", "J04 gives FAIL to P05", outcome,
              "4th vote received; P05 has 2 PASS / 2 FAIL and status becomes FAILED")

    result_view = ResultView(controller)
    result_view.display_summary()


if __name__ == "__main__":
    main()
