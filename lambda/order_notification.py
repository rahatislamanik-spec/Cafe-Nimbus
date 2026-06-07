"""
Cafe-Nimbus — Order Notification Lambda Function
AWS Lambda function for processing café orders and sending SNS notifications.

Triggered by: EventBridge scheduled rule (daily 8AM) or direct invocation
Publishes to: SNS topic (cafe-order-notifications)

This is a portfolio demonstration function — not connected to a live AWS environment.
"""

import json
import os
import boto3
from datetime import datetime


def validate_order(event: dict) -> tuple[bool, str]:
    """Validate required fields in the order event."""
    required_fields = ["order_id", "customer_name", "email", "items", "total"]
    
    for field in required_fields:
        if field not in event:
            return False, f"Missing required field: {field}"
    
    if not isinstance(event["items"], list) or len(event["items"]) == 0:
        return False, "Order must contain at least one item"
    
    if not isinstance(event["total"], (int, float)) or event["total"] <= 0:
        return False, "Order total must be a positive number"
    
    return True, "Valid"


def format_notification(order: dict) -> str:
    """Format a human-readable order notification message."""
    items_list = ", ".join(order["items"])
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    return (
        f"New Cafe-Nimbus Order\n"
        f"{'='*40}\n"
        f"Order ID:    {order['order_id']}\n"
        f"Customer:    {order['customer_name']}\n"
        f"Email:       {order['email']}\n"
        f"Items:       {items_list}\n"
        f"Total:       ${order['total']:.2f}\n"
        f"Timestamp:   {timestamp}\n"
        f"{'='*40}"
    )


def publish_to_sns(message: str, order_id: str) -> dict:
    """Publish notification to SNS topic."""
    topic_arn = os.environ.get("SNS_TOPIC_ARN")
    
    if not topic_arn:
        print("SNS_TOPIC_ARN not set — skipping SNS publish (dry run mode)")
        return {"skipped": True, "reason": "SNS_TOPIC_ARN not configured"}
    
    sns_client = boto3.client("sns")
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=f"New Order Received: {order_id}",
        MessageAttributes={
            "order_id": {
                "DataType": "String",
                "StringValue": order_id
            }
        }
    )
    
    return {"message_id": response["MessageId"], "published": True}


def lambda_handler(event: dict, context) -> dict:
    """
    Main Lambda handler.
    
    Expected event shape:
    {
        "order_id": "CF-10021",
        "customer_name": "Alex Morgan",
        "email": "alex@example.com",
        "items": ["Latte", "Blueberry Muffin"],
        "total": 12.75
    }
    """
    print(f"Processing order event: {json.dumps(event)}")
    
    # Validate order
    is_valid, validation_message = validate_order(event)
    if not is_valid:
        print(f"Validation failed: {validation_message}")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid order",
                "detail": validation_message
            })
        }
    
    # Format notification
    notification_message = format_notification(event)
    print(f"Formatted notification:\n{notification_message}")
    
    # Publish to SNS
    try:
        sns_result = publish_to_sns(notification_message, event["order_id"])
        print(f"SNS result: {sns_result}")
    except Exception as e:
        print(f"SNS publish failed: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Notification delivery failed",
                "detail": str(e)
            })
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Order processed successfully",
            "order_id": event["order_id"],
            "customer": event["customer_name"],
            "sns": sns_result
        })
    }


# Local test
if __name__ == "__main__":
    sample_event = {
        "order_id": "CF-10021",
        "customer_name": "Alex Morgan",
        "email": "alex@example.com",
        "items": ["Latte", "Blueberry Muffin"],
        "total": 12.75
    }
    result = lambda_handler(sample_event, None)
    print(f"\nResult: {json.dumps(result, indent=2)}")
