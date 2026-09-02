import json
from pathlib import Path
from .models import Opportunity


class LocalStateStore:
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
