import json
from pathlib import Path

from .models import Inquiry, Opportunity


class LocalStateStore:
    """Single-opportunity JSON store for the hackathon MVP.

    The interface is deliberately tiny so it can later be swapped for DynamoDB
    or another store without changing the agent tool contracts.
    """

    def __init__(self, path: str = "data/demo_state.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, opportunity: Opportunity) -> None:
        self.path.write_text(
            json.dumps(opportunity.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def load_raw(self) -> dict:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def load(self) -> Opportunity | None:
        raw = self.load_raw()
        if not raw:
            return None

        inquiry = Inquiry(**raw["inquiry"])
        payload = dict(raw)
        payload["inquiry"] = inquiry
        return Opportunity(**payload)

    def require(self, opportunity_id: str) -> Opportunity:
        opportunity = self.load()
        if opportunity is None:
            raise ValueError("No opportunity exists in local state.")
        if opportunity.id != opportunity_id:
            raise ValueError(
                f"Opportunity {opportunity_id!r} was not found; "
                f"current local opportunity is {opportunity.id!r}."
            )
        return opportunity
