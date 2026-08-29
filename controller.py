import json
from models import Judge, Contestant, Decision, STATUS_WAITING, STATUS_PASSED, STATUS_FAILED

TOTAL_JUDGES_PER_CONTESTANT = 4
MIN_PASS_TO_ADVANCE = 3


class ContestController:
    def __init__(self):
        self.judges: dict[str, Judge] = {}
        self.contestants: dict[str, Contestant] = {}

    @classmethod
    def load_from_seed(cls, seed_path: str) -> "ContestController":
        with open(seed_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        controller = cls()

        for j in data.get("judges", []):
            controller.judges[j["id"]] = Judge(j["id"], j["name"])

        for c in data.get("contestants", []):
            controller.contestants[c["id"]] = Contestant(c["id"], c["name"], c["performance"])

        for d in data.get("decisions", []):
            result = controller.submit_decision(d["judge_id"], d["contestant_id"], d["result"])
            if not result["success"]:
                raise ValueError(f"Invalid seed data: {result['message']}")

        for gb in data.get("golden_buzzers", []):
            result = controller.use_golden_buzzer(gb["judge_id"], gb["contestant_id"])
            if not result["success"]:
                raise ValueError(f"Invalid seed data: {result['message']}")

        return controller

    def list_contestants(self) -> list[Contestant]:
        return list(self.contestants.values())

    def get_contestant_detail(self, contestant_id: str) -> Contestant | None:
        return self.contestants.get(contestant_id)

    def submit_decision(self, judge_id: str, contestant_id: str, result: str) -> dict:
        judge = self.judges.get(judge_id)
        contestant = self.contestants.get(contestant_id)

        if judge is None:
            return self._fail(f"Judge {judge_id} not found")
        if contestant is None:
            return self._fail(f"Contestant {contestant_id} not found")
        if result not in ("PASS", "FAIL"):
            return self._fail("Result must be either PASS or FAIL")

        if not contestant.is_waiting():
            return self._fail(
                f"{contestant.name} has already been finalized as '{contestant.status}', cannot accept more decisions"
            )

        if judge_id in contestant.judged_by:
            return self._fail(
                f"{judge.name} has already judged or golden-buzzed {contestant.name}, cannot judge again"
            )

        decision = Decision(judge_id, contestant_id, result)
        contestant.decisions.append(decision)
        contestant.judged_by.add(judge_id)

        message = f"Recorded {result} from {judge.name} for {contestant.name}"

        if len(contestant.decisions) == TOTAL_JUDGES_PER_CONTESTANT:
            if contestant.pass_count() >= MIN_PASS_TO_ADVANCE:
                contestant.status = STATUS_PASSED
            else:
                contestant.status = STATUS_FAILED
            message += f" (all {TOTAL_JUDGES_PER_CONTESTANT} judges responded, finalized as '{contestant.status}')"

        return self._ok(message)

    def use_golden_buzzer(self, judge_id: str, contestant_id: str) -> dict:
        judge = self.judges.get(judge_id)
        contestant = self.contestants.get(contestant_id)

        if judge is None:
            return self._fail(f"Judge {judge_id} not found")
        if contestant is None:
            return self._fail(f"Contestant {contestant_id} not found")

        if judge.has_used_golden_buzzer:
            return self._fail(f"{judge.name} has already used their Golden Buzzer, cannot use it again")

        if not contestant.is_waiting():
            return self._fail(
                f"{contestant.name} has already been finalized as '{contestant.status}', cannot use Golden Buzzer"
            )

        if judge_id in contestant.judged_by:
            return self._fail(
                f"{judge.name} has already judged {contestant.name}, cannot use Golden Buzzer on them"
            )

        judge.has_used_golden_buzzer = True
        contestant.judged_by.add(judge_id)
        contestant.golden_buzzer_by = judge_id
        contestant.status = STATUS_PASSED

        return self._ok(
            f"{judge.name} used Golden Buzzer on {contestant.name}, advancing immediately "
            f"without waiting for the remaining judges"
        )

    def get_summary(self) -> list[dict]:
        summary = []
        for c in self.contestants.values():
            entry = {
                "id": c.contestant_id,
                "name": c.name,
                "status": c.status,
            }
            if c.golden_buzzer_by:
                entry["note"] = f"Advanced via Golden Buzzer from {self.judges[c.golden_buzzer_by].name}"
            elif c.status != STATUS_WAITING:
                entry["note"] = f"Advanced with {c.pass_count()}/{TOTAL_JUDGES_PER_CONTESTANT} PASS votes"
            else:
                entry["note"] = f"Received {len(c.decisions)}/{TOTAL_JUDGES_PER_CONTESTANT} votes so far"
            summary.append(entry)
        return summary

    @staticmethod
    def _ok(message: str) -> dict:
        return {"success": True, "message": message}

    @staticmethod
    def _fail(message: str) -> dict:
        return {"success": False, "message": message}
