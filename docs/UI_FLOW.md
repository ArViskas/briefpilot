# BriefPilot UI flow

This UI prototype is intentionally zero-cost and deterministic. It makes no AWS, Bedrock, Strands, email, website, or other external calls.

## Goal

Let a judge understand the product in under 30 seconds:

1. A vague client inquiry arrives.
2. BriefPilot extracts what it can.
3. It shows exactly what information is missing.
4. It prepares targeted clarification.
5. After the client reply, the opportunity becomes ready.
6. BriefPilot stops at a clear **Human decision required** boundary.

## Product rules represented in the prototype

- Routine intake work can be automated.
- The agent should not ask redundant questions.
- Agent actions should remain inspectable through an activity trail.
- Scope, pricing, deadlines, and final client commitments remain human-owned.
- The interface should feel like a focused workflow product, not a general chatbot or full CRM.

## Running the prototype

Open:

`prototype/index.html`

in a browser.

No package installation or server is required.

## What changes in the final build

The deterministic steps will be replaced by real AWS Strands Agents orchestration and real tool calls. The UI should keep the same visible states so the final demo remains easy to follow.
