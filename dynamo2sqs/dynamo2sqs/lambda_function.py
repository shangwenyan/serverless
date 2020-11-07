"""
Dynamo to SQS
"""
 
import boto3
import json
import sys
import os
 
DYNAMODB = boto3.resource('dynamodb')
TABLE = "fang"
QUEUE = "producer"
SQS = boto3.client("sqs")
 
 
def scan_table(table):
    """Scans table and return results"""
 
    producer_table = DYNAMODB.Table(table)
    response = producer_table.scan()
    items = response['Items']
    return items
 
def send_sqs_msg(msg, queue_name, delay=0):
    """Send SQS Message
 
    Expects an SQS queue_name and msg in a dictionary format.
    Returns a response dictionary. 
    """
 
    queue_url = SQS.get_queue_url(QueueName=queue_name)["QueueUrl"]
    queue_send_log_msg = "Send message to queue url: %s, with body: %s" %\
        (queue_url, msg)
    json_msg = json.dumps(msg)
    response = SQS.send_message(
        QueueUrl=queue_url,
        MessageBody=json_msg,
        DelaySeconds=delay)
    queue_send_log_msg_resp = "Message Response: %s for queue url: %s" %\
        (response, queue_url) 
    return response
 
def send_emissions(table, queue_name):
    """Send Emissions"""
 
    items = scan_table(table=table)
    for item in items:
        response = send_sqs_msg(item, queue_name=queue_name)

 
def lambda_handler(event, context):
    """
    Lambda entrypoint
    """
 
    extra_logging = {"table": TABLE, "queue": QUEUE}
    send_emissions(table=TABLE, queue_name=QUEUE)