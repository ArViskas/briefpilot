# BriefPilot

BriefPilot is an AI agent for freelancers and small studios that turns messy client inquiries into structured, qualified opportunities ready for human judgment.

## Hackathon

Built for the **Professional Agents** track of the **Agents for Humans Hackathon**.

Core principle:

> Clear the busywork, protect the judgment calls.

BriefPilot should autonomously handle routine intake work, but stop and escalate when a person needs to make a real decision such as confirming scope, pricing, deadlines, or a final client commitment.

## MVP flow

`New inquiry → Understand → Research → Clarify → Track → Escalate`

1. Receive a client inquiry.
2. Extract structured requirements.
3. Inspect client context when a URL is available.
4. Identify missing information.
5. Create or update a lead record.
6. Prepare clarification questions and follow-up.
7. Re-process the client reply.
8. Escalate a qualified opportunity to a human decision.

## Planned Strands tools

- `parse_inquiry`
- `inspect_site`
- `create_or_update_lead`
- `identify_missing_information`
- `send_clarification`
- `schedule_followup`
- `escalate_to_human`

The first scaffold intentionally runs without AWS model or runtime calls. The Strands integration is isolated in `src/briefpilot/agent.py` and will be enabled after hackathon promotional credits are confirmed.

## Local zero-cost demo

```bash
python -m src.briefpilot.mock_flow
```

This runs the deterministic demo fixture and writes local state to `data/demo_state.json`. No AWS API is called.

## Setup later

The official Strands Python quickstart currently requires Python 3.10+ and the `strands-agents` package. The final project will use Strands Agents as the agent framework and Amazon Bedrock for the hackathon build.

## Repository requirements before submission

- Public repository
- README
- Architecture diagram
- MIT or Apache open-source license
- All source code and setup instructions
- Working demo video, maximum 5 minutes
