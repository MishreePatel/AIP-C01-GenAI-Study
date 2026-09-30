"""
Cost & Performance Monitoring — Reference Implementation
------------------------------------------------------------
Demonstrates two things that matter for GenAI cost control on AWS:
1. Publishing token-usage metrics to CloudWatch after every model call,
   so cost is visible over time instead of discovered on the bill.
2. A simple in-memory cache so identical prompts don't get re-billed.

Domain: Cost & Performance
"""

import boto3
import hashlib
import time

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

NAMESPACE = "AIP-C01/BedrockUsage"


def publish_token_metrics(model_id: str, usage: dict):
    """
    Pushes input/output token counts to CloudWatch as custom metrics.
    Over time this is what lets you catch a cost spike (e.g. a prompt
    that suddenly got much longer) before it shows up as a surprise bill,
    and it's also how you'd set a CloudWatch Alarm to alert past a threshold.
    """
    cloudwatch.put_metric_data(
        Namespace=NAMESPACE,
        MetricData=[
            {
                "MetricName": "InputTokens",
                "Dimensions": [{"Name": "ModelId", "Value": model_id}],
                "Value": usage["inputTokens"],
                "Unit": "Count",
            },
            {
                "MetricName": "OutputTokens",
                "Dimensions": [{"Name": "ModelId", "Value": model_id}],
                "Value": usage["outputTokens"],
                "Unit": "Count",
            },
        ],
    )


class PromptCache:
    """
    A minimal cache keyed by a hash of the prompt text. If the exact same
    question comes in twice, the second call skips Bedrock entirely —
    zero tokens billed for a repeat question. A production system would
    back this with ElastiCache/DynamoDB instead of a Python dict so it
    survives restarts and is shared across instances.
    """

    def __init__(self, ttl_seconds: int = 3600):
        self._store = {}
        self.ttl = ttl_seconds

    def _key(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()

    def get(self, prompt: str):
        key = self._key(prompt)
        entry = self._store.get(key)
        if entry and (time.time() - entry["ts"] < self.ttl):
            return entry["value"]
        return None

    def set(self, prompt: str, value: str):
        self._store[self._key(prompt)] = {"value": value, "ts": time.time()}


def invoke_with_cache_and_metrics(prompt: str, cache: PromptCache, model_id: str):
    cached = cache.get(prompt)
    if cached is not None:
        print("Cache hit — no tokens billed for this call.")
        return cached

    response = bedrock.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 300, "temperature": 0.3},
    )
    answer = response["output"]["message"]["content"][0]["text"]
    usage = response["usage"]

    publish_token_metrics(model_id, usage)
    cache.set(prompt, answer)

    return answer


if __name__ == "__main__":
    cache = PromptCache()
    model = "anthropic.claude-3-5-haiku-20241022-v1:0"  # smaller model for routine, low-stakes queries

    print(invoke_with_cache_and_metrics("What AWS service runs serverless functions?", cache, model))
    # Second identical call — should hit the cache instead of calling Bedrock again.
    print(invoke_with_cache_and_metrics("What AWS service runs serverless functions?", cache, model))
