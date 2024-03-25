from pprint import pprint
import boto3
import json
import csv
import datetime
import os
import random
import base64
from decimal import Decimal
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    
    AWS_REGION = 'us-east-1'
    #print(event)
    
    dynamodb_res = boto3.resource('dynamodb', region_name=AWS_REGION)
    anomaly_table = dynamodb_res.Table('project6dynamodb')

    sns_client = boto3.client('sns', region_name=AWS_REGION)
    topic_arn = 'arn:aws:sns:us-east-1:007164637643:m03p02anomalyalerts'

    for record in event['Records']:
        data_point = base64.b64decode(record['kinesis']['data'])
        data_point = str(data_point, 'utf-8')
        pprint(data_point, sort_dicts=False)
        data_point = json.loads(data_point)
        anomaly_type = ''
        if data_point["value"] <= (1.01 * float(data_point['lowest_temp'])):
            anomaly_type = "Cold"
        elif data_point["value"] >= (0.99 * float(data_point['highest_temp'])):
            anomaly_type = "Hot"

        anomaly_data = {'deviceid': data_point["deviceid"], 
                            'anomalyDate': data_point["date"], 
                            'timestamp': data_point["timestamp"], 
                            'value': data_point["value"],
                            'anomalyType': anomaly_type}

        if len(anomaly_type) != 0:
            anomaly_data = json.loads(json.dumps(anomaly_data), parse_float=Decimal)
            response = anomaly_table.put_item(Item=anomaly_data)
            #pprint("DB Response Data: ", response)
            sns_client.publish(TopicArn=topic_arn, 
                                Message=str("Anomaly value = " + str(anomaly_data['value']) + " is detected. " + "Detcted temperature can be categorized as " + anomaly_data['anomalyType']) , 
                                Subject=str(anomaly_data['anomalyType'] + " temperature is detected.")
                                )
    return 1
