# Troubleshooting Guide — AWS GenAI Developer Labs

Real-world troubleshooting walkthroughs based on issues that come up when working with the artifacts in this repo (see [`technical-artifacts/`](.)).

---

## 1. Bedrock Converse API — `AccessDeniedException` on model invoke

**Scenario:** Calling `bedrock-runtime.converse()` with a specific model ID (e.g. an Anthropic model) to get a text response.

**Symptoms:**
```
botocore.errorfactory.AccessDeniedException: An error occurred (AccessDeniedException)
when calling the Converse operation: You don't have access to the model with the
specified model ID.
```

**Diagnosis:** Bedrock model access is opt-in per model, per AWS account, per region. Having IAM permission to call `bedrock:InvokeModel` is not the same as having been granted access to that specific foundation model — Bedrock keeps these as two separate checks.

**Fix:**
1. Go to the Bedrock console → **Model access** (left sidebar)
2. Request access to the specific model (e.g. Anthropic Claude models)
3. Wait for status to flip from `Available to request` → `Access granted`
4. Confirm the `region_name` in the boto3 client matches a region where that model is actually offered — not every model is available in every region

**Verification:** Re-run the script; `response["output"]["message"]["content"]` returns text instead of raising.

---

## 2. RAG pipeline — retrieved chunks are irrelevant to the question

**Scenario:** Running the manual RAG pipeline (`2_rag_pipeline.py`) and getting back chunks that don't actually relate to the question asked.

**Symptoms:** `answer_with_rag()` returns "I don't know" or an off-topic answer, even though the source document clearly contains the relevant fact.

**Diagnosis:** Two usual suspects — (1) `chunk_size` too large, so a chunk contains multiple unrelated facts and its embedding becomes a "blurry average" that doesn't score well against a specific question, or (2) `chunk_size` too small, so the fact gets cut off across a chunk boundary and neither half contains the full context.

**Fix:**
- Reduce chunk size to isolate single facts/ideas per chunk, and keep `overlap` at roughly 10-20% of chunk size so a boundary cut doesn't lose context
- Increase `top_k` in `store.search()` so more candidate chunks reach the prompt instead of only the single best (sometimes imperfect) match

**Verification:** Print the retrieved chunks with their similarity scores (already done in the `if __name__` block) and confirm the top-ranked chunk actually contains the answer before it reaches the model.

---

## 3. Bedrock Agent — action group never gets invoked

**Scenario:** The agent (`4_bedrock_agent_definition.py`) answers order-status questions by guessing instead of calling the `check_order_status` Lambda.

**Symptoms:** Agent responds with a generic or made-up answer; CloudWatch Logs for the Lambda function show zero invocations.

**Diagnosis:** The agent decides whether to call an action purely from the wording in `apiSchema` (the `summary` and `description` fields) matched against the user's question. A vague schema description means the agent can't tell the tool is relevant, so it falls back to answering from the model alone.

**Fix:**
- Make `summary`/`description` in the OpenAPI schema specific and phrased the way a user would actually ask (e.g. "Look up the current status of a customer order" rather than just "Order endpoint")
- Confirm the agent alias has been re-prepared after any schema change — a stale `DRAFT` version won't pick up schema edits

**Verification:** Ask the agent a question closely matching the schema's wording, then check the Lambda's CloudWatch Logs to confirm an invocation occurred before the response was generated.

---

## 4. Guardrails config — blocks legitimate requests

**Scenario:** Applying the guardrail from `3_guardrails_config.json` and finding normal, safe questions getting blocked.

**Symptoms:** Response returns `blockedInputMessaging` text ("I can't help with that request.") for input that isn't actually unsafe.

**Diagnosis:** Filter strength was set too aggressively (e.g. `HIGH` on a category like `INSULTS` or `MISCONDUCT`) for the actual use case, causing false positives on borderline phrasing.

**Fix:** Lower `inputStrength`/`outputStrength` for the filter category causing false positives from `HIGH` → `MEDIUM`, test against a small set of known-safe prompts that were previously blocked, and only raise strength back up if abuse is actually observed.

**Verification:** Re-run the same previously-blocked, legitimate prompt and confirm it now returns a normal model response instead of the blocked-input message.

---

## 5. Cost monitoring — CloudWatch metrics never appear

**Scenario:** Calling `publish_token_metrics()` after every model invocation in `5_cost_monitoring.py`, but the custom metric namespace never shows up in the CloudWatch console.

**Symptoms:** `AIP-C01/BedrockUsage` namespace is missing from CloudWatch → Metrics → All metrics, even after several script runs.

**Diagnosis:** CloudWatch custom metrics can take a few minutes to appear after the first `put_metric_data` call, and separately, the IAM role/user running the script may be missing the `cloudwatch:PutMetricData` permission — which fails silently in some SDK configurations if errors aren't explicitly checked.

**Fix:**
- Wait 1-2 minutes after first publish before checking the console (metric namespaces are created lazily)
- Explicitly wrap the `put_metric_data` call and print any exception to confirm it isn't failing silently
- Confirm the IAM policy attached includes `cloudwatch:PutMetricData` on `Resource: "*"`

**Verification:** Namespace `AIP-C01/BedrockUsage` appears in the CloudWatch console with `InputTokens`/`OutputTokens` data points matching the number of script runs.
