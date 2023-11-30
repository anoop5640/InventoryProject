# your_app/aws_utils.py

import boto3
from botocore.exceptions import ClientError

def create_sns_topic(topic_name):
    """Create an SNS topic and return its ARN."""
    sns_client = boto3.client('sns', region_name='us-east-1')

    try:
        response = sns_client.create_topic(Name=topic_name)
        return response['TopicArn']
    except ClientError as e:
        print(e)
        return None

def publish_to_sns_topic(topic_arn, message, subject):
    """Publish a message to an SNS topic."""
    sns_client = boto3.client('sns', region_name='us-east-1')

    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        return response
    except ClientError as e:
        print(e)
        return None
