"""
Bedrock Model Invocation — Reference Implementation
-----------------------------------------------------
Demonstrates how to call a foundation model in Amazon Bedrock using the
Converse API (the current recommended way to invoke models — it works
across model providers with one consistent request/response shape,
instead of each model having its own custom JSON body).

Domain: Foundation Models, Data & RAG
"""

import boto3
import json

# The bedrock-runtime client is used for INFERENCE (actually calling a model).
# This is different from the plain "bedrock" client, which is used for
# management tasks like listing available models or creating guardrails.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"  # swap for any Bedrock model ID


def invoke_model(user_prompt: str, system_prompt: str = None, max_tokens: int = 512):
    """
    Calls a Bedrock model with the Converse API.

    Why Converse instead of invoke_model():
    - invoke_model() needs a different JSON body shape per model provider
      (Anthropic's body looks different from Meta's or Amazon Titan's).
    - converse() normalizes all of that into one shape, so switching models
      later (e.g. testing a cheaper model for cost reasons) doesn't require
      rewriting the request.
    """
    messages = [
        {
            "role": "user",
            "content": [{"text": user_prompt}],
        }
    ]

    kwargs = {
        "modelId": MODEL_ID,
        "messages": messages,
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": 0.3,   # lower temperature = more deterministic, good for factual tasks
            "topP": 0.9,
        },
    }

    if system_prompt:
        kwargs["system"] = [{"text": system_prompt}]

    response = client.converse(**kwargs)

    output_text = response["output"]["message"]["content"][0]["text"]
    usage = response["usage"]  # inputTokens / outputTokens / totalTokens — useful for cost tracking

    return output_text, usage


if __name__ == "__main__":
    answer, token_usage = invoke_model(
        user_prompt="In two sentences, explain what a foundation model is.",
        system_prompt="You are a concise AWS technical instructor.",
    )
    print("MODEL RESPONSE:\n", answer)
    print("\nTOKEN USAGE:\n", json.dumps(token_usage, indent=2))
