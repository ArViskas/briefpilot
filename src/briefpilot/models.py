from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class Inquiry:
    raw_text: str
    client_name: Optional[str] = None
    company: Optional[str] = None
    website_url: Optional[str] = None
    requested_work: List[str] = field(default_factory=list)
    platform: Optional[str] = None
    timeline: Optional[str] = None
    budget_signal: Optional[str] = None
    references: List[str] = field(default_factory=list)


@dataclass
class Opportunity:
    id: str
    status: str
    inquiry: Inquiry
    missing_information: List[str] = field(default_factory=list)
    client_context: dict = field(default_factory=dict)
    clarification_questions: List[str] = field(default_factory=list)
    recommended_next_action: Optional[str] = None
    main_risk: Optional[str] = None
    draft_reply: Optional[str] = None

    def to_dict(self):
        return asdict(self)
