# How to explain each artifact (30-second version each)

## 1. Bedrock model invocation
"This calls a foundation model using the Converse API — it's the newer,
unified way to call any Bedrock model with the same request shape, instead
of writing custom JSON for each model provider. I pass a system prompt, a
user prompt, and get back the model's text plus token usage, which matters
for cost."

## 2. RAG pipeline
"This builds RAG from scratch instead of using the managed Knowledge Base
service, to show I understand the steps underneath it: split a document
into overlapping chunks, turn each chunk into a vector with an embedding
model, store those vectors, then at query time embed the question and find
the closest matching chunks by cosine similarity, and stuff those chunks
into the prompt so the model answers from real data instead of guessing."

## 3. Guardrails config
"This is the config you'd send to create a Bedrock Guardrail. It has four
layers: denied topics the model won't touch, content filters for things
like hate/violence at different strength levels, PII detection that masks
or blocks sensitive data, and a word blocklist. It checks both what the
user sends in and what the model sends back."

## 4. Bedrock Agent definition
"This shows how an agent goes from 'just answers questions' to 'can take
action.' The instruction tells it how to behave, the action group is an
OpenAPI schema that tells it when and how to call a tool, and that tool is
backed by a real Lambda function — here, one that looks up an order status
instead of the model just guessing an answer."

## 5. Cost & performance monitoring
"Two cost controls: first, every model call publishes its input/output
token counts to CloudWatch as a custom metric, so usage is visible over
time instead of showing up as a surprise on the bill. Second, a prompt
cache — if the exact same question comes in twice, the second one is
served from cache with zero tokens billed."
