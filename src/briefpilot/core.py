import re
from .models import Inquiry, Opportunity


def parse_demo_inquiry(raw_text: str) -> Inquiry:
    urls = re.findall(r"https?://[^\s,]+", raw_text)
    lower = raw_text.lower()

    platform = "WooCommerce" if "woocommerce" in lower else None
    requested = []
    if "redesign" in lower:
        requested.append("redesign")
    if "discount" in lower or "promotion" in lower:
        requested.append("discount visibility")

    return Inquiry(
        raw_text=raw_text.strip(),
        company="Demo Client",
        website_url=urls[0] if urls else None,
        requested_work=requested,
        platform=platform,
        timeline=None,
        budget_signal=None,
        references=[],
    )


def identify_missing_information(inquiry: Inquiry) -> list[str]:
    missing = []
    if not inquiry.website_url:
        missing.append("current website URL")
    if not inquiry.timeline:
        missing.append("desired timeline")
    missing.append("whether the work covers only the homepage or also product/cart experience")
    return missing


def build_clarification_questions(missing: list[str]) -> list[str]:
    questions = []
    for item in missing[:3]:
        if item == "current website URL":
            questions.append("Could you share the current store URL?")
        elif item == "desired timeline":
            questions.append("Is there a target launch date or preferred timeline?")
        elif "homepage" in item:
            questions.append(
                "Should the redesign cover only the homepage, or also product and cart/checkout discount presentation?"
            )
    return questions


def qualify(inquiry: Inquiry, opportunity_id: str = "BP-DEMO-001") -> Opportunity:
    missing = identify_missing_information(inquiry)
    questions = build_clarification_questions(missing)
    return Opportunity(
        id=opportunity_id,
        status="needs_clarification" if missing else "qualified",
        inquiry=inquiry,
        missing_information=missing,
        clarification_questions=questions,
        recommended_next_action="Ask the client for the missing details.",
        main_risk="Scope is not yet precise enough for a commercial commitment.",
    )


def apply_demo_client_reply(opportunity: Opportunity, reply_text: str) -> Opportunity:
    opportunity.inquiry.website_url = opportunity.inquiry.website_url or "https://example-shop.test"
    opportunity.inquiry.timeline = "3 weeks"
    opportunity.missing_information = []
    opportunity.clarification_questions = []
    opportunity.status = "human_decision_required"
    opportunity.client_context = {
        "site_type": "existing WooCommerce store",
        "observed_scope_signal": "homepage + discount visibility across shopping journey",
    }
    opportunity.main_risk = "Existing custom checkout logic should be reviewed before committing scope."
    opportunity.recommended_next_action = "Human technical review before confirming scope and price."
    opportunity.draft_reply = (
        "Thanks — I have enough context for the next step. "
        "I’d first review the existing store structure and checkout logic, "
        "then confirm the exact scope, timing, and price."
    )
    return opportunity
