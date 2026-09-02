"""Framework-agnostic BriefPilot tool contracts.

These functions are deliberately independent from Strands. The final Strands
@tool wrappers should call this layer so product rules remain testable without
an AWS model call.
"""

from datetime import datetime, timezone
from .core import (
    apply_client_reply,
    build_clarification_questions,
    identify_missing_information,
    parse_demo_inquiry,
    qualify,
)
from .models import Inquiry, Opportunity


HUMAN_ONLY_ACTIONS = {
    "confirm_scope",
    "set_price",
    "commit_deadline",
    "send_final_proposal",
}


def parse_inquiry(raw_text: str) -> Inquiry:
    return parse_demo_inquiry(raw_text)


def inspect_site(url: str) -> dict:
    """Zero-cost placeholder.

    The final implementation may inspect public web context, but it must stay
    bounded and read-only. This function intentionally makes no network call.
    """
    return {
        "url": url,
        "status": "not_called_zero_cost_scaffold",
        "mode": "read_only",
        "note": "Real safe site inspection will be implemented before final demo.",
    }


def create_or_update_lead(inquiry: Inquiry, opportunity_id: str = "BP-DEMO-001") -> Opportunity:
    return qualify(inquiry, opportunity_id=opportunity_id)


def identify_missing_information_tool(inquiry: Inquiry) -> list[str]:
    return identify_missing_information(inquiry)


def prepare_clarification(missing: list[str]) -> list[str]:
    return build_clarification_questions(missing)


def receive_client_reply(opportunity: Opportunity, reply_text: str) -> Opportunity:
    return apply_client_reply(opportunity, reply_text)


def schedule_followup(opportunity: Opportunity, due_at_iso: str) -> Opportunity:
    # Validate basic ISO-8601 shape without triggering any external scheduler.
    datetime.fromisoformat(due_at_iso.replace("Z", "+00:00"))
    opportunity.followup_due_at = due_at_iso
    opportunity.activity.append(f"Follow-up scheduled for {due_at_iso}")
    return opportunity


def escalation_summary(opportunity: Opportunity) -> dict:
    return {
        "opportunity_id": opportunity.id,
        "status": opportunity.status,
        "main_risk": opportunity.main_risk,
        "recommended_next_action": opportunity.recommended_next_action,
        "human_decision_reasons": list(opportunity.human_decision_reasons),
        "draft_reply": opportunity.draft_reply,
    }


def may_execute_without_human(action: str) -> bool:
    return action not in HUMAN_ONLY_ACTIONS


def current_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
