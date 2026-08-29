STATUS_WAITING = "WAITING"
STATUS_PASSED = "PASSED"
STATUS_FAILED = "FAILED"


class Judge:
    def __init__(self, judge_id: str, name: str):
        self.judge_id = judge_id
        self.name = name
        self.has_used_golden_buzzer = False

    def __repr__(self):
        return f"Judge({self.judge_id}, {self.name})"


class Decision:
    def __init__(self, judge_id: str, contestant_id: str, result: str):
        self.judge_id = judge_id
        self.contestant_id = contestant_id
        self.result = result

    def __repr__(self):
        return f"Decision({self.judge_id} -> {self.contestant_id}: {self.result})"


class Contestant:
    def __init__(self, contestant_id: str, name: str, performance: str):
        self.contestant_id = contestant_id
        self.name = name
        self.performance = performance
        self.status = STATUS_WAITING
        self.decisions: list[Decision] = []
        self.judged_by: set[str] = set()
        self.golden_buzzer_by: str | None = None

    def pass_count(self) -> int:
        return sum(1 for d in self.decisions if d.result == "PASS")

    def fail_count(self) -> int:
        return sum(1 for d in self.decisions if d.result == "FAIL")

    def is_waiting(self) -> bool:
        return self.status == STATUS_WAITING

    def __repr__(self):
        return f"Contestant({self.contestant_id}, {self.name}, status={self.status})"
