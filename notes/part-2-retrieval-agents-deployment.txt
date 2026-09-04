Part 2 — Retrieval, Agents & Deployment

🔗 Video: https://youtu.be/DqHoQXvx6AU?si=_T3jWmqJCSrmbHDw

Topics Covered

1. Vector Stores, RAG & Prompt Governance
- Vector stores: Amazon OpenSearch Service, Bedrock Knowledge Bases, Aurora with pgvector
- RAG pipeline: `document → chunk → embed → vector DB → retrieve → inject into prompt → grounded answer`
- Chunking strategy and embedding model choice directly affect retrieval quality
- Bedrock Prompt Management & Prompt Flows for versioning, approvals, reusable templates

2. Agentic AI & Tool Integration
- Agents break a task into steps and call external tools/APIs to complete it
- Amazon Bedrock AgentCore + Strands Agents for memory, state, and orchestration
- Model Context Protocol (MCP) standardizes tool discovery and calling
- Safeguards: timeouts, stopping conditions, circuit breakers

3. Model Deployment & Enterprise Integration
- Deployment options: Lambda (on-demand), Bedrock provisioned throughput (predictable latency), SageMaker AI endpoints (custom models)
- Enterprise integration: API Gateway, event-driven architectures (EventBridge), webhooks
- Identity federation & role-based access control (least privilege)
- CI/CD pipelines (CodePipeline/CodeBuild) with security scans and rollback support

Labs Completed
- [x] Built a RAG pipeline (Bedrock Knowledge Base / FAISS) with document ingestion
- [x] Created a Bedrock Agent with a Lambda-backed action group
- [x] Free AWS workshop: agent + Knowledge Base + RAG

Key Takeaways
> RAG lets a model answer questions about your private data without retraining it.

> An agent is a model plus a controlled way for it to act — not just a chat interface.

> A GenAI feature isn't "done" until it's deployed, connected, and safe to update in production.
