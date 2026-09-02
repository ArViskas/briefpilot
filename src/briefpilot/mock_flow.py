from pathlib import Path

from .core import parse_demo_inquiry, qualify, apply_demo_client_reply
from .state import LocalStateStore


def main():
    inquiry_text = Path("data/demo_inquiry.txt").read_text(encoding="utf-8")
    reply_text = Path("data/demo_client_reply.txt").read_text(encoding="utf-8")

    inquiry = parse_demo_inquiry(inquiry_text)
    opportunity = qualify(inquiry)

    print("1. INQUIRY RECEIVED")
    print(f"   status: {opportunity.status}")
    print("   missing:")
    for item in opportunity.missing_information:
        print(f"   - {item}")

    print("\n2. CLARIFICATION QUESTIONS")
    for q in opportunity.clarification_questions:
        print(f"   - {q}")

    opportunity = apply_demo_client_reply(opportunity, reply_text)

    print("\n3. CLIENT REPLY PROCESSED")
    print(f"   status: {opportunity.status}")

    print("\n4. HUMAN DECISION REQUIRED")
    print(f"   main risk: {opportunity.main_risk}")
    print(f"   next action: {opportunity.recommended_next_action}")
    print(f"   draft reply: {opportunity.draft_reply}")

    store = LocalStateStore()
    store.save(opportunity)
    print("\nSaved local demo state to data/demo_state.json")


if __name__ == "__main__":
    main()
