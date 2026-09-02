import re
from .models import Inquiry, Opportunity


URL_RE = re.compile(r"https?://[^\s,]+")
TIMELINE_PATTERNS = (
    (re.compile(r"\b(?:in|within|around)\s+(\d+)\s+weeks?\b", re.I), "weeks"),
    (re.compile(r"\b(?:in|within|around)\s+(\d+)\s+days?\b", re.I), "days"),
)


def _extract_url(text: str) -> str | None:
    matches = URL_RE.findall(text)
    return matches[0].rstrip(".);]") if matches else None


def _extract_timeline(text: str) -> str | None:
    for pattern, unit in TIMELINE_PATTERNS:
        match = pattern.search(text)
        if match:
            amount = int(match.group(1))
            label = unit[:-1] if amount == 1 else unit
            return f"{amount} {label}"
    return None


def _extract_scope_signals(text: str) -> list[str]:
    lower = text.lower()
    signals: list[str] = []
    candidates = [
        ("homepage", "homepage"),
        ("product page", "product pages"),
        ("product pages", "product pages"),
        ("cart", "cart"),
        ("checkout", "checkout"),
        ("discount", "discount visibility"),
        ("promotion", "discount visibility"),
    ]
    for needle, label in candidates:
        if needle in lower and label not in signals:
            signals.append(label)
    return signals


def parse_demo_inquiry(raw_text: str) -> Inquiry:
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
        website_url=_extract_url(raw_text),
        requested_work=requested,
        platform=platform,
        timeline=_extract_timeline(raw_text),
        budget_signal=None,
        references=[],
        scope_signals=_extract_scope_signals(raw_text),
    )


def identify_missing_information(inquiry: Inquiry) -> list[str]:
    missing = []
    if not inquiry.website_url:
        missing.append("current website URL")
    if not inquiry.timeline:
        missing.append("desired timeline")

    has_commerce_scope = any(
        signal in inquiry.scope_signals
        for signal in ("product pages", "cart", "checkout")
    )
    if not has_commerce_scope:
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
        recommended_next_action=(
            "Ask the client for the missing details."
            if missing
            else "Review the qualified opportunity."
        ),
        main_risk=(
            "Scope is not yet precise enough for a commercial commitment."
            if missing
            else None
        ),
        activity=[
            "Inquiry received",
            "Requirements extracted",
            f"{len(missing)} missing detail(s) identified" if missing else "No blocking intake gaps found",
        ],
    )


def apply_client_reply(opportunity: Opportunity, reply_text: str) -> Opportunity:
    url = _extract_url(reply_text)
    timeline = _extract_timeline(reply_text)
    scope_signals = _extract_scope_signals(reply_text)

    if url:
        opportunity.inquiry.website_url = url
    if timeline:
        opportunity.inquiry.timeline = timeline
    for signal in scope_signals:
        if signal not in opportunity.inquiry.scope_signals:
            opportunity.inquiry.scope_signals.append(signal)

    opportunity.missing_information = identify_missing_information(opportunity.inquiry)
    opportunity.clarification_questions = build_clarification_questions(
        opportunity.missing_information
    )
    opportunity.activity.extend([
        "Client reply received",
        "Opportunity updated",
    ])

    if opportunity.missing_information:
        opportunity.status = "needs_clarification"
        opportunity.main_risk = "Required intake details are still missing."
        opportunity.recommended_next_action = "Ask only for the remaining missing details."
        opportunity.draft_reply = None
        opportunity.human_decision_reasons = []
        return opportunity

    opportunity.status = "human_decision_required"
    opportunity.client_context = {
        "site_type": (
            "existing WooCommerce store"
            if opportunity.inquiry.platform == "WooCommerce"
            else "existing website"
        ),
        "observed_scope_signal": " + ".join(opportunity.inquiry.scope_signals)
        if opportunity.inquiry.scope_signals
        else "scope clarified by client",
    }
    opportunity.main_risk = (
        "Existing checkout or commerce logic should be reviewed before committing scope."
        if any(
            signal in opportunity.inquiry.scope_signals
            for signal in ("cart", "checkout", "product pages")
        )
        else "Technical scope should be reviewed before a commercial commitment."
    )
    opportunity.recommended_next_action = (
        "Human technical review before confirming scope, price, and deadline."
    )
    opportunity.human_decision_reasons = [
        "confirm final scope",
        "set price",
        "commit delivery timeline",
        "approve final commercial reply",
    ]
    opportunity.draft_reply = (
        "Thanks — I have enough context for the next step. "
        "I’d first review the existing store structure and relevant commerce logic, "
        "then confirm the exact scope, timing, and price."
    )
    opportunity.activity.append("Human decision required")
    return opportunity


# Backwards-compatible name used by the original zero-cost demo.
apply_demo_client_reply = apply_client_reply
