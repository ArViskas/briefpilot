from src.briefpilot.core import (
    apply_client_reply,
    parse_demo_inquiry,
    qualify,
)
from src.briefpilot.tools import (
    escalation_summary,
    may_execute_without_human,
    schedule_followup,
)


def test_demo_flow_reaches_human_decision():
    raw = (
        "We have an existing WooCommerce shop and want to redesign "
        "the homepage and make discounts more visible."
    )
    inquiry = parse_demo_inquiry(raw)
    opp = qualify(inquiry)

    assert opp.status == "needs_clarification"
    assert len(opp.missing_information) == 3

    opp = apply_client_reply(
        opp,
        (
            "The store is https://example-shop.test. "
            "We need homepage, product pages and cart changes within 3 weeks."
        ),
    )

    assert opp.status == "human_decision_required"
    assert opp.missing_information == []
    assert opp.inquiry.website_url == "https://example-shop.test"
    assert opp.inquiry.timeline == "3 weeks"
    assert "cart" in opp.inquiry.scope_signals
    assert opp.main_risk
    assert opp.draft_reply
    assert "set price" in opp.human_decision_reasons


def test_partial_reply_asks_only_for_remaining_gaps():
    inquiry = parse_demo_inquiry(
        "WooCommerce redesign for homepage and discount visibility."
    )
    opp = qualify(inquiry)

    opp = apply_client_reply(
        opp,
        "The current website is https://example-shop.test.",
    )

    assert opp.status == "needs_clarification"
    assert opp.missing_information == [
        "desired timeline",
        "whether the work covers only the homepage or also product/cart experience",
    ]
    assert len(opp.clarification_questions) == 2


def test_human_only_actions_are_blocked_from_autonomy():
    assert may_execute_without_human("send_clarification") is True
    assert may_execute_without_human("inspect_site") is True
    assert may_execute_without_human("set_price") is False
    assert may_execute_without_human("commit_deadline") is False
    assert may_execute_without_human("send_final_proposal") is False


def test_followup_is_recorded_locally_without_external_action():
    inquiry = parse_demo_inquiry("WooCommerce redesign.")
    opp = qualify(inquiry)

    opp = schedule_followup(opp, "2026-09-05T09:00:00+03:00")

    assert opp.followup_due_at == "2026-09-05T09:00:00+03:00"
    assert opp.activity[-1].startswith("Follow-up scheduled")


def test_escalation_summary_exposes_decision_boundary():
    inquiry = parse_demo_inquiry(
        "WooCommerce redesign. Store: https://example-shop.test. "
        "Need homepage, product pages and cart work within 3 weeks."
    )
    opp = qualify(inquiry)

    # No intake gaps remain, but commercial commitment still belongs to a human.
    if opp.status == "qualified":
        opp = apply_client_reply(opp, "")

    summary = escalation_summary(opp)

    assert summary["status"] == "human_decision_required"
    assert "set price" in summary["human_decision_reasons"]


def test_agent_layer_is_hard_disabled_without_flag(monkeypatch):
    monkeypatch.setenv("BRIEFPILOT_ENABLE_AWS", "false")

    from src.briefpilot.agent import aws_enabled, build_agent

    assert aws_enabled() is False

    try:
        build_agent()
    except RuntimeError as exc:
        assert "promotional credits" in str(exc)
    else:
        raise AssertionError("build_agent() must stay disabled before credits are confirmed")


def test_local_state_round_trip(tmp_path):
    from src.briefpilot.state import LocalStateStore

    inquiry = parse_demo_inquiry(
        "WooCommerce redesign for homepage discount visibility."
    )
    opp = qualify(inquiry)

    store = LocalStateStore(str(tmp_path / "state.json"))
    store.save(opp)
    loaded = store.require(opp.id)

    assert loaded.id == opp.id
    assert loaded.inquiry.platform == "WooCommerce"
    assert loaded.missing_information == opp.missing_information
