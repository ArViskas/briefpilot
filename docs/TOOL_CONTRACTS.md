# Tool contracts and human boundary

BriefPilot's business logic is kept separate from Strands orchestration so the
workflow can be tested locally without making an AWS model call.

## Planned agent-facing tools

| Tool | Purpose | Autonomous? |
| --- | --- | --- |
| `parse_inquiry` | Extract deterministic structure before/around agent reasoning | Yes |
| `inspect_site` | Read-only bounded website context | Yes |
| `create_or_update_lead` | Maintain opportunity state | Yes |
| `identify_missing_information` | Find blocking intake gaps | Yes |
| `prepare_clarification` | Ask only necessary questions | Yes |
| `receive_client_reply` | Update state from the client's response | Yes |
| `schedule_followup` | Record a future follow-up | Yes, within configured policy |
| `escalation_summary` | Package the decision-ready opportunity for a human | Yes |

## Human-only decisions

BriefPilot must not autonomously:

- confirm final scope;
- set or commit a price;
- commit a delivery deadline;
- send a final commercial proposal.

These boundaries live in code as `HUMAN_ONLY_ACTIONS` so they can be tested,
not just described in a prompt.

## Current zero-cost state

- No Bedrock call.
- No AgentCore deployment.
- No email send.
- No website fetch.
- No external scheduler.
- All tests and demo logic run locally.

When promotional credits are confirmed, Strands `@tool` wrappers can be added
around these contracts without changing the core product rules.
