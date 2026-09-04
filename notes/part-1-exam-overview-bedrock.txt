Part 1  — Exam Overview & Amazon Bedrock Fundamentals

🔗 Video: https://youtu.be/A2ofxaqvNFs?si=IgYmwJZdYNuXeN-Q

Topics Covered

1. What Is the AIP-C01 Exam?
- Professional-level certification for developers who build production GenAI applications on AWS
- Tests integration of foundation models (FMs) into real applications — not model training itself
- 65 scored questions + 10 unscored, scaled passing score of 750/1000
- Content organized into 5 weighted domains

2. Amazon Bedrock Fundamentals
- Unified API for accessing multiple foundation models (Anthropic, Amazon, and others)
- Model selection based on capability, cost, and latency trade-offs
- Inference parameters (temperature, top-p/top-k) tune output creativity/determinism
- Invocation via console (testing), SDK (boto3), and CLI (production use)

3. FM Integration & Data Pipelines
- Data validation and cleanup before reaching a foundation model
- AWS Glue Data Quality / SageMaker Data Wrangler for catching data quality issues
- Formatting input to match each model's expected request structure (e.g., JSON for Bedrock APIs)
- Entity extraction & text normalization for response consistency

Labs Completed
- AWS Free Tier setup + enabled Bedrock model access
- Invoked a model via console and boto3/CLI
- Prompting playground: zero-shot, one-shot, few-shot, chain-of-thought exercises

Key Takeaways
> This exam is about implementation and integration skill, not building models from scratch.

> Everything else in this exam — RAG, agents, guardrails — is built on top of Bedrock model invocation.

> Garbage in, garbage out still applies to GenAI — pipeline quality directly drives response quality.
