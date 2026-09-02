# VŽ AI Engineer Sprint

## Goal

Evolve BriefPilot into a small but real AI engineering portfolio project that demonstrates the core skills requested in the Verslo Žinios AI Engineer role without overstating experience.

The project should remain useful as a Kitoki internal tool: turn a vague client inquiry into a structured brief, retrieve relevant internal knowledge, propose a scope/estimate, draft a response, and stop for human approval before any client-facing commitment.

## Why BriefPilot

The existing repository already has:
- Python project structure
- deterministic intake logic
- agent/tool abstractions
- tests
- architecture/tooling docs
- clickable prototype
- a human-escalation product principle

This sprint extends that foundation rather than creating a throwaway RAG demo.

## Target architecture

Client / UI
  -> FastAPI API
  -> Intake + agent orchestration
  -> RAG retrieval
  -> PostgreSQL + pgvector
  -> LLM provider abstraction
       - cloud provider for deployed demo
       - Ollama option for local/self-hosted inference
  -> deterministic tools
       - parse inquiry
       - retrieve knowledge
       - calculate estimate
       - create/update lead
       - draft proposal
  -> human approval gate

## Core technical scope

### 1. Python / FastAPI
- FastAPI service
- Pydantic request/response models
- async endpoints where useful
- explicit error handling, timeouts, and health endpoint

### 2. RAG
- ingest a small curated Kitoki knowledge base
- chunk and embed source documents
- store embeddings in pgvector
- retrieve top relevant chunks
- return source citations with generated answers
- keep retrieval separate from user instructions

### 3. Agent + tools
- model can call only allow-listed tools
- tool inputs validated with schemas
- business calculations remain deterministic
- no direct sending or irreversible client action
- final proposal requires human approval

### 4. Model providers
- cloud LLM provider for the deployed demo
- Ollama provider option for local/self-hosted testing
- provider interface so inference can be swapped without changing business logic

### 5. Security
- secrets only in environment variables
- prompt-injection test cases
- untrusted inquiry text explicitly separated from trusted system/knowledge instructions
- retrieved documents treated as data, not executable instructions
- tool allow-list and input validation
- human approval before client-facing commitment
- no arbitrary shell/file/network tool

### 6. Reliability / observability
- structured logs
- request IDs
- retries/timeouts around model calls
- health/readiness endpoint
- predictable failure responses
- cost/token logging where supported

### 7. Testing + evals
- existing deterministic unit tests preserved
- API tests
- retrieval tests
- a small eval set of representative client inquiries
- prompt-injection/adversarial tests
- expected structured fields and citation checks

### 8. Deployment / DevOps
- Dockerfile
- docker-compose for API + PostgreSQL/pgvector
- GitHub Actions for tests/lint
- deployed demo
- documented local Linux/Docker commands

## Seven-day target

Day 1
- lock architecture and branch
- add FastAPI skeleton
- Docker + pgvector local stack
- health endpoint and test

Day 2
- knowledge ingestion
- embeddings
- pgvector retrieval
- citations

Day 3
- connect RAG to intake flow
- model provider abstraction
- cloud model integration
- structured outputs

Day 4
- agent/tool calling
- deterministic estimate tool
- human approval state
- Ollama local provider

Day 5
- security hardening
- injection tests
- logs/timeouts/error handling
- eval set

Day 6
- UI/API integration
- deployment
- CI/CD
- end-to-end tests

Day 7
- README + architecture diagram
- demo scenario/video
- interview notes: explain every technical choice in plain language
- CV wording only after verification of what actually works

## Explicit non-goals

- claiming senior AI/ML engineering experience
- Kubernetes/Terraform/GPU administration unless actually implemented
- building a generic "chat with PDF" toy
- letting the model decide prices without deterministic business rules
- letting the agent send messages or take irreversible actions without approval
- overengineering before the end-to-end flow works

## Definition of done

A reviewer can clone the repo, run the documented Docker setup, ingest the sample knowledge base, submit a client inquiry, see retrieved sources, receive a structured brief and draft proposal, observe a human-approval gate, run tests/evals, and understand the security and deployment choices from the README.
