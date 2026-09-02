from src.briefpilot.core import (
    parse_demo_inquiry,
    qualify,
    apply_demo_client_reply,
)


def test_demo_flow_reaches_human_decision():
    raw = (
        "We have an existing WooCommerce shop and want to redesign "
        "the homepage and make discounts more visible."
    )
    inquiry = parse_demo_inquiry(raw)
    opp = qualify(inquiry)

    assert opp.status == "needs_clarification"
    assert len(opp.missing_information) >= 2

    opp = apply_demo_client_reply(
        opp,
        "The store is https://example-shop.test and launch is in three weeks.",
    )

    assert opp.status == "human_decision_required"
    assert opp.missing_information == []
    assert opp.main_risk
    assert opp.draft_reply
