Part 3— Safety, Cost & Evaluation

🔗 Video: https://youtu.be/dJ5CI_DAXu4?si=9hNpPiPwwdFtpp4E

Topics Covered

1. AI Safety, Security & Responsible AI
- Guardrails flow: `user input → guardrail (input check) → foundation model → guardrail (output check) → safe response`
- Amazon Bedrock Guardrails: denied topics, harmful content filtering, prompt injection defense
- Data privacy: Amazon Comprehend & Macie for PII detection/masking
- Governance: data lineage tracking, CloudTrail logging for audits, model cards
- Responsible AI: transparency, fairness evaluation, documented model limitations

 2. Cost, Performance & Monitoring
- Token usage drives cost — prompt compression, context pruning, response limits
- Right-sized model selection (tiering requests by complexity) instead of always using the largest model
- Semantic caching to avoid paying for near-identical repeated calls
- CloudWatch: token usage, latency, response quality tracking + anomaly detection

3. Evaluation & Troubleshooting
- Evaluation beyond accuracy: relevance, factual accuracy, consistency, fluency
- LLM-as-a-judge: using a foundation model to score another model's outputs at scale
- RAG evaluation: retrieval relevance and generation quality assessed separately
- Common failure points: context window overflow, prompt confusion, embedding/retrieval drift

Labs Completed
- [x] Added Guardrails (input/output filtering, denied topics) to the Week 2 agent
- [x] CloudWatch monitoring pass: token usage & invocation logs
- [x] AWS "Agentic AI Demonstrated" microcredential (free, hands-on)

Key Takeaways
> Safety and governance aren't an add-on step — they're built into the request/response flow itself.

> The most capable model isn't always the right choice — cost-aware design is a tested skill here.

> When something goes wrong, the fix is usually in retrieval, the prompt, or the data — rarely the model itself.

---

🎓 This wraps up the AIP-C01 study series. See the main [README](../README.md) for the full progress tracker and video links.
