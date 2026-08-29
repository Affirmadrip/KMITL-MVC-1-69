from controller import ContestController


class EntryView:
    def __init__(self, controller: ContestController):
        self.controller = controller

    def display_contestants(self):
        print("\n=== Contestants ===")
        for c in self.controller.list_contestants():
            print(f"  {c.contestant_id}  {c.name:<20} {c.performance:<20} Status: {c.status}")

    def display_contestant_detail(self, contestant_id: str):
        c = self.controller.get_contestant_detail(contestant_id)
        if c is None:
            print(f"Contestant {contestant_id} not found")
            return
        print(f"\n=== {c.name} ({c.contestant_id}) ===")
        print(f"  Performance: {c.performance}")
        print(f"  Status: {c.status}")
        print(f"  Votes received: {len(c.decisions)}/4 (PASS {c.pass_count()}, FAIL {c.fail_count()})")
        if c.golden_buzzer_by:
            print(f"  Advanced via Golden Buzzer from judge: {c.golden_buzzer_by}")

    def submit_decision(self, judge_id: str, contestant_id: str, result: str):
        outcome = self.controller.submit_decision(judge_id, contestant_id, result)
        self._print_outcome(outcome)
        return outcome

    def use_golden_buzzer(self, judge_id: str, contestant_id: str):
        outcome = self.controller.use_golden_buzzer(judge_id, contestant_id)
        self._print_outcome(outcome)
        return outcome

    @staticmethod
    def _print_outcome(outcome: dict):
        tag = "OK" if outcome["success"] else "REJECTED"
        print(f"  [{tag}] {outcome['message']}")


class ResultView:
    def __init__(self, controller: ContestController):
        self.controller = controller

    def display_summary(self):
        print("\n=== Final Summary ===")
        for entry in self.controller.get_summary():
            print(f"  {entry['id']}  {entry['name']:<20} {entry['status']:<10} ({entry['note']})")
