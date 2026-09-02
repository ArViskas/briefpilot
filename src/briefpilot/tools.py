from .core import (
    parse_demo_inquiry,
    identify_missing_information,
    build_clarification_questions,
)


def parse_inquiry(raw_text: str):
    return parse_demo_inquiry(raw_text)


def inspect_site(url: str) -> dict:
    return {
        "url": url,
        "status": "not_called_zero_cost_scaffold",
        "note": "Real safe site inspection will be implemented before final demo.",
    }


def identify_missing(inquiry):
    return identify_missing_information(inquiry)


def clarification_questions(missing):
    return build_clarification_questions(missing)
