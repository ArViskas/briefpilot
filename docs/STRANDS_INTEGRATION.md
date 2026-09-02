# Strands integration plan

The real Strands integration layer now exists in `src/briefpilot/agent.py`, but
it is deliberately gated so zero-cost preparation cannot accidentally invoke AWS.

## Current safety behavior

`build_agent()` refuses to construct the Strands Agent unless:

`BRIEFPILOT_ENABLE_AWS=true`

The default in `.env.example` is `false`.

Strands is imported lazily inside `build_agent()`, so normal local tests and
the deterministic prototype do not require the SDK and do not contact AWS.

## Planned Strands tools

- `create_lead`
- `inspect_client_site`
- `get_clarification_questions`
- `update_from_client_reply`
- `record_followup`
- `escalate_for_human_decision`

Each wrapper delegates to the framework-agnostic tool contracts already tested
in `src/briefpilot/tools.py`.

## Why this structure

The hackathon evaluates meaningful Strands use, but BriefPilot's product and
safety rules should not live only inside an LLM prompt. Keeping deterministic
business rules beneath the Strands wrappers gives us:

- testable human approval boundaries;
- inspectable state transitions;
- easier local debugging;
- a clean path to swap local JSON storage later;
- less risk of accidental external actions during development.

## When credits are confirmed

1. Install the optional agent dependencies:
   `pip install -e ".[agent,dev]"`
2. Configure AWS credentials with Bedrock permissions.
3. Confirm the selected Bedrock model and region.
4. Set `BRIEFPILOT_ENABLE_AWS=true`.
5. Construct the agent.
6. Run the first controlled invocation against the demo fixture.
7. Verify tool calls and AWS cost before expanding the workflow.

No step above should be performed before the credits confirmation unless the
user explicitly chooses to use existing AWS credits.
