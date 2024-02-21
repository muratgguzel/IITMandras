import json
import boto3
import base64
from decimal import Decimal

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Project5_DynomoDb')  

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

        
        if within_twenty_percent_of_high or within_twenty_five_percent_of_low:
            # Update payload with Decimal types
            payload["price"] = price
            payload["52WeekHigh"] = high_52week
            payload["52WeekLow"] = low_52week
            payload["price_timestamp"] = str(payload["price_timestamp"])  
            
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
