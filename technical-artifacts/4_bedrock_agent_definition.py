"""
Bedrock Agent Definition — Reference Implementation
------------------------------------------------------
Demonstrates how a Bedrock Agent is structured: instructions that define
its behavior, and an action group that gives it a real tool it can call
(here, a Lambda function that checks order status). This is what turns a
model from "answers questions" into "can actually go do something."

Domain: Building & Connecting It (Implementation & Integration)
"""

import boto3

bedrock_agent = boto3.client("bedrock-agent", region_name="us-east-1")

AGENT_INSTRUCTION = (
    "You are a customer support agent for an online store. "
    "When a customer asks about an order, use the check_order_status "
    "action to look up real order data before answering. "
    "Never guess an order status — always call the tool."
)

# ---------- Action group schema ----------
# This is the OpenAPI-style schema Bedrock uses to know WHEN to call the tool
# and WHAT parameters to pass it. The agent reads this schema, matches it
# against the user's question, and decides whether invoking the action
# will help answer it.
ACTION_GROUP_SCHEMA = {
    "openapi": "3.0.0",
    "info": {"title": "Order Status API", "version": "1.0.0"},
    "paths": {
        "/check_order_status": {
            "get": {
                "summary": "Look up the current status of a customer order.",
                "operationId": "check_order_status",
                "parameters": [
                    {
                        "name": "order_id",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"},
                        "description": "The customer's order ID, e.g. ORD-10293.",
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Order status returned successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string"},
                                        "estimated_delivery": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            }
        }
    },
}


def create_agent():
    """Creates the agent itself — the 'brain' with instructions, but no tools yet."""
    response = bedrock_agent.create_agent(
        agentName="order-support-agent",
        instruction=AGENT_INSTRUCTION,
        foundationModel="anthropic.claude-3-5-sonnet-20241022-v2:0",
        idleSessionTTLInSeconds=600,
    )
    return response["agent"]["agentId"]


def attach_action_group(agent_id: str, lambda_arn: str):
    """
    Attaches the action group (the tool) to the agent, pointing it at a
    Lambda function that actually performs the lookup. This is the step
    that gives the agent a real capability instead of just instructions.
    """
    response = bedrock_agent.create_agent_action_group(
        agentId=agent_id,
        agentVersion="DRAFT",
        actionGroupName="order-status-lookup",
        actionGroupExecutor={"lambda": lambda_arn},
        apiSchema={"payload": str(ACTION_GROUP_SCHEMA)},
    )
    return response["agentActionGroup"]["actionGroupId"]


# ---------- Lambda handler (deployed separately as the action's executor) ----------
def lambda_handler(event, context):
    """
    This is the Lambda function referenced by attach_action_group() above.
    Bedrock calls this function when the agent decides it needs order data.
    """
    order_id = event["parameters"][0]["value"]

    # In a real system this would query a database (e.g. DynamoDB).
    fake_orders_db = {
        "ORD-10293": {"status": "Shipped", "estimated_delivery": "2026-10-03"},
    }
    order = fake_orders_db.get(order_id, {"status": "Not found", "estimated_delivery": None})

    return {
        "response": {
            "actionGroup": event["actionGroup"],
            "apiPath": event["apiPath"],
            "httpMethod": event["httpMethod"],
            "httpStatusCode": 200,
            "responseBody": {"application/json": {"body": str(order)}},
        }
    }


if __name__ == "__main__":
    agent_id = create_agent()
    attach_action_group(agent_id, lambda_arn="arn:aws:lambda:us-east-1:123456789012:function:check-order-status")
    print(f"Agent created: {agent_id}")
