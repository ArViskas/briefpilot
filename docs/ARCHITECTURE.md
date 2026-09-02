# Architecture draft

```mermaid
flowchart LR
    A[Client inquiry] --> B[BriefPilot UI / intake]
    B --> C[Strands Agent]
    C --> D[parse_inquiry]
    C --> E[inspect_site]
    C --> F[create_or_update_lead]
    C --> G[identify_missing_information]
    C --> H[send_clarification]
    C --> I[schedule_followup]
    C --> J[escalate_to_human]

    D --> K[(Opportunity state)]
    E --> K
    F --> K
    G --> K
    H --> K
    I --> K

    K --> C
    C --> L{Judgment required?}
    L -- No --> M[Continue routine workflow]
    L -- Yes --> N[Human decision required]
    N --> O[Scope / price / deadline / final reply]
```

## Zero-cost scaffold

Current implementation:
- Python core logic
- Local JSON state
- Deterministic demo fixture
- Strands integration isolated and disabled by default

No AWS model or runtime call occurs in this stage.

## Target final implementation

- **Agent framework:** AWS Strands Agents
- **Model provider:** Amazon Bedrock
- **State:** local JSON initially; optional DynamoDB if useful
- **Frontend:** React + TypeScript
- **Deployment:** live web demo
- **Stretch:** Amazon Bedrock AgentCore Runtime

## Safety boundary

BriefPilot may autonomously perform routine intake actions, but must escalate before:
- committing a price;
- confirming final scope;
- committing a deadline;
- sending a final commercial proposal;
- making irreversible external changes.
