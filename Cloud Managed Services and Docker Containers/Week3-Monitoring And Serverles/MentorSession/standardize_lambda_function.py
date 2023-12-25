from pprint import pprint
import boto3
import json
import csv
import datetime
import os
import random


def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')

    eventText = json.dumps(event)

    standardized = eventText.replace('datatype', 'type').replace('deviceid', 'device_id')
    standardized_data = json.loads(standardized)

    table = dynamodb_res.Table('BedsideStandardized')
    response = table.put_item(Item=standardized_data)

    pprint(response, sort_dicts=False)