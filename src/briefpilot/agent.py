import os

AWS_ENABLED = os.getenv("BRIEFPILOT_ENABLE_AWS", "false").lower() == "true"


def build_agent():
    if not AWS_ENABLED:
        raise RuntimeError(
            "AWS agent calls are disabled. Set BRIEFPILOT_ENABLE_AWS=true only "
            "after promotional credits are confirmed."
        )

    from strands import Agent, tool

    @tool
    def identify_missing_information_tool(summary: str) -> str:
        return f"Review missing information for: {summary}"

    return Agent(
        tools=[identify_missing_information_tool],
        system_prompt=(
            "You are BriefPilot, a client-intake agent for freelancers and small studios. "
            "Handle routine intake work autonomously. Never commit scope, pricing, deadlines, "
            "or final client promises without escalating to a human."
        ),
    )
