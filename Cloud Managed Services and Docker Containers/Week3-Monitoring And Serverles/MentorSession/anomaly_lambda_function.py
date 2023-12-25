from pprint import pprint
import boto3
import json
import csv
import datetime
import os
import random
import base64


def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')

    for record in event['records']:
        payload = base64.b64decode(record['data'])
        payload = str(payload, 'utf-8')
        pprint(payload, sort_dicts=False)

        payload_std = payload.replace('DEVICEID', 'deviceid').replace('DATATYPE', 'datatype').replace('COL_TIMESTAMP',
                                                                                                      'timestamp').replace(
            'COL_VALUE', 'value')

        payload_rec = json.loads(payload_std)
        pprint(payload_rec, sort_dicts=False)

        table = dynamodb_res.Table('BedsideAnomalies')
        response = table.put_item(Item=payload_rec)

        client = boto3.client('sns', region_name='us-east-1')
        topic_arn = "arn:aws:sns:us-east-1:989319265633:bedside-anomaly"

        try:
            client.publish(TopicArn=topic_arn, Message="heart rate detected over 90", Subject="heartrate90+")
            result = 1
        except Exception:
            result = 0

    return result