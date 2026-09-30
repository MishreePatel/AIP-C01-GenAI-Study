# AWS Certified Generative AI Developer – Professional (AIP-C01) — Study Log

Public study log and video series notes for my prep towards the **AWS Certified Generative AI Developer – Professional (AIP-C01)** certification.

This repo tracks the topics I studied, the hands-on labs I completed, and the companion YouTube video series I'm recording as I go.
   ## 🔗 Connect

   - 💼 LinkedIn: [Post about this series](https://lnkd.in/p/g4aWYGiN)
   - 📺 Latest video: [The 5 Core Domains, Explained](https://youtu.be/GiK27gLML7Y)

## 🎯 Why this repo

I'm documenting this journey publicly so it can:
- Serve as a study reference for others prepping for AIP-C01
- Act as a portfolio piece showing hands-on work with Amazon Bedrock, RAG, agentic AI, and GenAI application design on AWS
- Keep me accountable to a study schedule

## 📺 Video Series

| Part | Topics | Video |
|------|--------|-------|
| Part 1 | Exam overview, Amazon Bedrock fundamentals, FM integration & data pipelines | 🔗 https://youtu.be/A2ofxaqvNFs?si=9Xk5jdvQeqiW508O |
| Part 2 | Vector stores & RAG, agentic AI & tool integration, model deployment & enterprise integration | 🔗 https://youtu.be/DqHoQXvx6AU?si=rBgRF307pas8oOgZ |
| Part 3 | AI safety & security, cost & performance monitoring, evaluation & troubleshooting | 🔗 https://youtu.be/dJ5CI_DAXu4?si=2T3ymoo1NNZOY6Zu |
| Wrap-up | The 5 Core Domains, explained simply | 🔗 https://youtu.be/GiK27gLML7Y |

Slide decks for each part are in [`/presentations`](./presentations).

## 📚 Study Progress

## 🧪 Technical Artifacts

Reference implementations demonstrating hands-on understanding of core AWS GenAI services, one per major domain. These are written to show how each piece works under the hood rather than only using the fully-managed version of each service.

| Artifact | Domain | What it shows |
|---|---|---|
| [`1_bedrock_invoke.py`](technical-artifacts/1_bedrock_invoke.py) | Foundation Models | Calling a Bedrock model via the Converse API |
| [`2_rag_pipeline.py`](technical-artifacts/2_rag_pipeline.py) | Foundation Models & RAG | RAG built from scratch — chunking, embedding, vector search, retrieval-augmented generation |
| [`3_guardrails_config.json`](technical-artifacts/3_guardrails_config.json) | AI Safety & Governance | A Bedrock Guardrails configuration — denied topics, content filters, PII handling, word blocklist |
| [`4_bedrock_agent_definition.py`](technical-artifacts/4_bedrock_agent_definition.py) | Implementation & Integration | A Bedrock Agent with an action group backed by a real Lambda function |
| [`5_cost_monitoring.py`](technical-artifacts/5_cost_monitoring.py) | Cost & Performance | CloudWatch token-usage metrics and a prompt cache to reduce redundant model calls |

See [`TROUBLESHOOTING.md`](technical-artifacts/TROUBLESHOOTING.md) for real issues encountered while building these and how they were resolved.

### Week 1
- [x] Amazon Bedrock fundamentals (model access, configuration, invocation via console/API/SDK)
- [x] Domain 1 foundations — FM integration architecture & data validation pipelines

**Labs completed:**
- [x] AWS Free Tier setup + enabling Bedrock model access
- [x] Invoking a model via console and boto3/CLI
- [x] Prompting techniques playground (zero-shot, one-shot, few-shot, chain-of-thought)


- [x] Vector stores, RAG & prompt governance
- [x] Agentic AI & tool integration (Bedrock AgentCore, Strands Agents, MCP)
- [x] Model deployment & enterprise integration

**Labs completed:**
- [x] Built a RAG pipeline (Bedrock Knowledge Base / FAISS)
- [x] Bedrock Agent with a Lambda-backed action group
- [x] Free AWS workshop: agent + knowledge base + RAG


- [x] AI safety, security & responsible AI (Guardrails)
- [x] Cost, performance & monitoring
- [x] Evaluation & troubleshooting

**Labs completed:**
- [x] Added Guardrails to the Week 2 agent
- [x] CloudWatch monitoring pass on token usage & invocation logs
- [x] AWS "Agentic AI Demonstrated" microcredential

See detailed notes per part in [`/notes`](./notes).

## 🗂️ Repo Structure

```
aip-c01-genai-study/
├── README.md                # this file — overview & progress tracker
├── notes/                   # topic-by-topic study notes, one file per video part
  ├── part-1-exam-overview-bedrock.md
  ├── part-2-retrieval-agents-deployment.md
  └── part-3-safety-cost-evaluation.md
├── technical-artifacts/   # Reference code & configs for core AWS GenAI services

```

## 🛠️ Key AWS Services Covered

`Amazon Bedrock` · `Bedrock Knowledge Bases` · `Bedrock Guardrails` · `Bedrock AgentCore` · `Amazon OpenSearch Service` · `Aurora (pgvector)` · `AWS Lambda` · `Amazon SageMaker AI` · `Amazon CloudWatch` · `Amazon Comprehend` · `Amazon Macie` · `API Gateway`

## 📌 Exam Info

- **Exam code:** AIP-C01
- **Format:** 65 scored questions + 10 unscored, scaled passing score of 750/1000
- **Level:** Professional
- **Focus:** Integrating foundation models into real, production GenAI applications — not model training/fine-tuning

## 🙏 Acknowledgements

Thank you to my professor for the guidance and support throughout this learning journey.

## 📄 License

Notes and slides in this repo are shared under [MIT License](./LICENSE) unless noted otherwise — feel free to reference them for your own study, with attribution appreciated.
