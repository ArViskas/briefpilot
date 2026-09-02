"""Strands orchestration layer for BriefPilot.

This file is intentionally safe to keep in the repository before credits arrive:
- importing it does not import Strands;
- importing it does not construct an Agent;
- importing it does not call AWS;
- build_agent() hard-fails unless BRIEFPILOT_ENABLE_AWS=true.

The @tool wrappers are created only inside build_agent().
"""

import os

from .state import LocalStateStore
from .tools import (
    create_or_update_lead,
    escalation_summary,
    inspect_site,
    prepare_clarification,
    receive_client_reply,
    schedule_followup,
)


SYSTEM_PROMPT = """
You are BriefPilot, a professional client-intake agent for freelancers and small studios.

Your job is to clear repetitive intake work while protecting human judgment.

Workflow:
1. Turn a messy inquiry into a structured opportunity.
2. Identify only the information that is actually missing.
3. Use read-only context tools when relevant.
4. Prepare targeted clarification rather than generic questions.
5. Update the opportunity when the client replies.
6. Escalate when final scope, price, delivery commitment, or a final commercial reply requires human judgment.

Never:
- invent client facts;
- commit final scope;
- set or commit a price;
- commit a delivery deadline;
- send a final commercial proposal on behalf of the human.

Prefer concise tool use and make the workflow inspectable.
""".strip()


def aws_enabled() -> bool:
    return os.getenv("BRIEFPILOT_ENABLE_AWS", "false").lower() == "true"


def build_agent(state_path: str = "data/demo_state.json"):
    """Build the real Strands agent without invoking it.

    Agent construction is gated behind BRIEFPILOT_ENABLE_AWS so the project can
    be prepared locally while promotional credits are pending.
    """
    if not aws_enabled():
        raise RuntimeError(
            "AWS agent construction is disabled. "
            "Set BRIEFPILOT_ENABLE_AWS=true only after promotional credits are confirmed."
        )

    # Lazy import: zero-cost local tests do not require Strands to be installed.
    from strands import Agent, tool

    store = LocalStateStore(state_path)

    @tool
    def create_lead(raw_text: str) -> dict:
        """Create a structured opportunity from a raw client inquiry.

        Args:
            raw_text: The client's original inquiry text.

        Returns:
            The current opportunity state as JSON-compatible data.
        """
        inquiry = __import__(
            "src.briefpilot.tools", fromlist=["parse_inquiry"]
        ).parse_inquiry(raw_text)
        opportunity = create_or_update_lead(inquiry)
        store.save(opportunity)
        return opportunity.to_dict()

    @tool
    def inspect_client_site(url: str) -> dict:
        """Inspect client website context in read-only mode.

        Args:
            url: Public website URL supplied by the client.

        Returns:
            Bounded read-only inspection data.
        """
        return inspect_site(url)

    @tool
    def get_clarification_questions(opportunity_id: str) -> dict:
        """Return only the clarification questions still needed.

        Args:
            opportunity_id: Existing BriefPilot opportunity ID.

        Returns:
            Missing information and targeted clarification questions.
        """
        opportunity = store.require(opportunity_id)
        return {
            "opportunity_id": opportunity.id,
            "missing_information": list(opportunity.missing_information),
            "questions": prepare_clarification(opportunity.missing_information),
        }

    @tool
    def update_from_client_reply(opportunity_id: str, reply_text: str) -> dict:
        """Update an opportunity using a client's reply.

        Args:
            opportunity_id: Existing BriefPilot opportunity ID.
            reply_text: New reply text from the client.

        Returns:
            Updated opportunity state.
        """
        opportunity = store.require(opportunity_id)
        opportunity = receive_client_reply(opportunity, reply_text)
        store.save(opportunity)
        return opportunity.to_dict()

    @tool
    def record_followup(opportunity_id: str, due_at_iso: str) -> dict:
        """Record a future follow-up without contacting the client.

        Args:
            opportunity_id: Existing BriefPilot opportunity ID.
            due_at_iso: ISO-8601 timestamp for the follow-up.

        Returns:
            Updated opportunity state.
        """
        opportunity = store.require(opportunity_id)
        opportunity = schedule_followup(opportunity, due_at_iso)
        store.save(opportunity)
        return opportunity.to_dict()

    @tool
    def escalate_for_human_decision(opportunity_id: str) -> dict:
        """Package a decision-ready opportunity for human review.

        Args:
            opportunity_id: Existing BriefPilot opportunity ID.

        Returns:
            Risk, next action, human-only decisions, and draft reply.
        """
        opportunity = store.require(opportunity_id)
        return escalation_summary(opportunity)

    model_id = os.getenv("BRIEFPILOT_MODEL_ID")
    kwargs = {
        "tools": [
            create_lead,
            inspect_client_site,
            get_clarification_questions,
            update_from_client_reply,
            record_followup,
            escalate_for_human_decision,
        ],
        "system_prompt": SYSTEM_PROMPT,
    }
    if model_id:
        kwargs["model"] = model_id

    return Agent(**kwargs)
