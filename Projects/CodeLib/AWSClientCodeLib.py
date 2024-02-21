import csv
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import os
import json

# Here we assign our aws clients/resources to use
iot_client = boto3.client('iot',region_name ='us-east-1')
s3 = boto3.resource(service_name = 's3')
dynamodb_resource = boto3.resource('dynamodb',region_name='us-east-1')
table = dynamodb_resource.Table('bsmcloudtest')

# Getting current date and previous date
current_date = datetime.date.today()
previous_date = current_date - datetime.timedelta(days=1)
prevDay = previous_date.day
prevMonth = previous_date.month
prevYear = previous_date.year


# retrive unique device ids from the IOT Core 
response = iot_client.list_things(maxResults=100, thingTypeName='HealthCare')
devices = response["things"]

device_ids = []
for y in devices:
	    device_id = y["thingName"]
	    device_ids.append(device_id)

for device_id in device_ids:
        #condition = Key('deviceid').eq(device_id)& Key('timestamp').between('2021-03-19','2021-03-20')
        condition = Key('deviceid').eq(device_id)& Key('timestamp').between(str(previous_date),str(current_date))
        responsevalues = table.query(KeyConditionExpression=condition)
        if len(responsevalues['Items']) != 0:
                items = responsevalues['Items']
                columns = items[0].keys()
                key = "HealthCareDataArchive/"+ device_id + "/" + str(prevYear) + "/" + str(prevMonth) + "/"
                filename = device_id + "-" + str(prevYear) + "-" + str(prevMonth) + "-" + str(prevDay) + ".csv"
                with open(filename,'a') as f:
                        dict_writer = csv.DictWriter(f, columns)
                        dict_writer.writeheader()
                        for i in items:
                                dict_writer.writerow(i)
                s3.meta.client.upload_file(Filename = filename,Bucket="healthdata",Key=key+filename)



from pprint import pprint
import boto3
import json
import csv
import datetime
import os
import random

LAMBDA

def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')

    eventText = json.dumps(event)

    standardized = eventText.replace('datatype', 'type').replace('deviceid', 'device_id')
    standardized_data = json.loads(standardized)

    table = dynamodb_res.Table('BedsideStandardized')
    response = table.put_item(Item=standardized_data)

    pprint(response, sort_dicts=False)

KINESIS 

import boto3
import time
import json
from decimal import Decimal

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('bsmanomalytable')

client = boto3.client('kinesis')
shardIterator = client.get_shard_iterator(
    StreamName='BSMStream',
    ShardId='shardId-000000000000',
    ShardIteratorType='LATEST',
)['ShardIterator']

while True:
    response = client.get_records(
        ShardIterator=shardIterator
    )
    shardIterator = response['NextShardIterator']
    if len(response['Records']) > 0:
        for item in response['Records']:
            readings = json.loads(item["Data"], parse_float=Decimal)
        print(readings)

        if (readings['datatype'] == 'HeartRate') and ((60 > int(readings['value'])) or (int(readings['value']) > 100)):
            table.put_item(Item=readings)
            print("Anomaly detected, entry added in DynamoDB Table")
        elif (readings['datatype'] == 'SPO2') and ((85 > int(readings['value'])) or (int(readings['value']) > 110)):
            table.put_item(Item=readings)
            print("Anomaly detected, entry added in DynamoDB Table")
        elif (readings['datatype'] == 'Temperature') and ((96 > int(readings['value'])) or (int(readings['value']) > 101)):
            table.put_item(Item=readings)
            print("Anomaly detected, entry added in DynamoDB Table")
    time.sleep(0.2)


import json
import boto3
import sys
import yfinance as yf

import time
import random
import datetime


# Your goal is to get per-hour stock price data for a time range for the ten stocks specified in the doc. 
# Further, you should call the static info api for the stocks to get their current 52WeekHigh and 52WeekLow values.
# You should craft individual data records with information about the stockid, price, price timestamp, 52WeekHigh and 52WeekLow values and push them individually on the Kinesis stream

kinesis = boto3.client('kinesis', region_name = "us-east-1") #Modify this line of code according to your requirement.

today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(1)

# Example of pulling the data between 2 dates from yfinance API
data = yf.download("MSFT", start= yesterday, end= today, interval = '1h' )

## Add code to pull the data for the stocks specified in the doc


## Add additional code to call 'info' API to get 52WeekHigh and 52WeekLow refering this this link - https://pypi.org/project/yfinance/


## Add your code here to push data records to Kinesis stream.



#LAMBDA FUNCTION

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
        topic_arn = "arn:aws:sns:us-east-1:007164637643:Project5_SNS:d5dbff4e-86fe-46ef-8818-72155a4d4a9f"

        try:
            client.publish(TopicArn=topic_arn, Message="heart rate detected over 90", Subject="heartrate90+")
            result = 1
        except Exception:
            result = 0

    return result


#Second Lambda Function

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


    import json

def lambda_handler(event, context):
    
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')
    
    for record in event['records']:
        payload = base64.b64decode(record['data'])
        payload = str(payload, 'utf-8')
        pprint(payload, sort_dicts=False)
        
        payload_rec = json.loads(payload)
        
        table = dynamodb_res.Table('Project5_DynomoDb')
        response = table.put_item(Item=payload_rec)
    
    return result


import json
import boto3
import base64
from decimal import Decimal

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Project5_DynomoDb')  # Replace 'StockPrices' with your table name

def lambda_handler(event, context):
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        encoded_data = record["kinesis"]["data"]
        decoded_data = base64.b64decode(encoded_data)
        payload = json.loads(decoded_data)
        
        # Convert to Decimal for DynamoDB compatibility
        payload["price"] = Decimal(str(payload["price"]))
        payload["52WeekHigh"] = Decimal(str(payload["52WeekHigh"]))
        payload["52WeekLow"] = Decimal(str(payload["52WeekLow"]))
        
        # Insert into DynamoDB
        table.put_item(Item=payload)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed records.')
    }


LAST WORKING Code


import json
import boto3
import base64
from decimal import Decimal

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Project5_DynomoDb')  # Ensure this is your table name

def lambda_handler(event, context):
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        encoded_data = record["kinesis"]["data"]
        decoded_data = base64.b64decode(encoded_data)
        payload = json.loads(decoded_data)
        
        # Convert numeric values to Decimal for DynamoDB compatibility
        payload["price"] = Decimal(str(payload["price"]))
        payload["52WeekHigh"] = Decimal(str(payload["52WeekHigh"]))
        payload["52WeekLow"] = Decimal(str(payload["52WeekLow"]))
        
        # Ensure price_timestamp is properly formatted as a string (assuming it is already)
        # If it's not a string, convert or format it as needed
        payload["price_timestamp"] = str(payload["price_timestamp"])
        
        # Insert into DynamoDB
        table.put_item(Item=payload)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed records.')
    }


import json
import boto3
import base64
from decimal import Decimal

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Project5_DynomoDb')  # Ensure this is your table name

# Initialize the SNS client
sns_client = boto3.client('sns', region_name='us-east-1')

topic_arn = "arn:aws:sns:us-east-1:007164637643:Project5_SNS"

def lambda_handler(event, context):
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        encoded_data = record["kinesis"]["data"]
        decoded_data = base64.b64decode(encoded_data)
        payload = json.loads(decoded_data)
        
        # Convert numeric values to Decimal for DynamoDB compatibility
        price = Decimal(str(payload["price"]))
        high_52week = Decimal(str(payload["52WeekHigh"]))
        low_52week = Decimal(str(payload["52WeekLow"]))
        
        # Calculate thresholds
        within_twenty_percent_of_high = high_52week * Decimal('0.80') <= price <= high_52week
        within_twenty_five_percent_of_low = low_52week <= price <= low_52week * Decimal('1.25')

        # Check if the price is within the specified range using "or"
        if within_twenty_percent_of_high or within_twenty_five_percent_of_low:
            # Update payload with Decimal types
            payload["price"] = price
            payload["52WeekHigh"] = high_52week
            payload["52WeekLow"] = low_52week
            payload["price_timestamp"] = str(payload["price_timestamp"])  # Ensure price_timestamp is formatted as a string
            
            # Insert into DynamoDB
            table.put_item(Item=payload)

            # Construct the message for SNS notification
            message = f"Stock {payload['stockid']} is currently priced at {price}, meeting one of the targeted criteria: " \
                      f"either within 20% of the 52-week high or within 25% of the 52-week low."

            # Publish to SNS topic
            sns_client.publish(TopicArn=topic_arn, Message=message)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed records.')
    }
