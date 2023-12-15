import boto3
import time
import typing as t
import json
from decimal import Decimal
from pathlib import Path
from IoTAnalytics.Config.core import DATASET_DIR, PROCESS_DIR, config
from datetime import datetime, timedelta
import time
import statistics
from datetime import datetime, timedelta
import time
import statistics
import boto3
from botocore.exceptions import ClientError
import statistics
from boto3.dynamodb.conditions import Key
import json



def aggregate_heart_rate_data(DeviceId):
    """
    Aggregate heart rate data between start_time and end_time.

    :param table_name: Name of the DynamoDB table.
    :param start_time: Start time for data aggregation (timestamp string in ISO format).
    :param end_time: End time for data aggregation (timestamp string in ISO format).
    """

    # Usage
    dynamodb = boto3.resource(config.app_config.Resource)
    #Raw Data Table
    table = dynamodb.Table(config.app_config.Raw_Dynamo_Table)
    #Aggregate Table
    target_tabel=dynamodb.Table(config.app_config.Aggregate_Dynamo_Table)

    response = table.query(KeyConditionExpression=Key('deviceid').eq(DeviceId) & Key('timestamp').between(config.app_config.StartTime,config.app_config.EndTime))
    items = response['Items']
    print(items)

    heart_rates = []
    SPO2_array=[]
    Temprature_array=[]

    for item in response['Items']:
        datatype_content = item.get('datatype', None)
        print(f"datatype content: {datatype_content}")  # Log the content for debugging

        if datatype_content=="HeartRate":
            try:
                heart_rate = int(item.get('value', None))
                heart_rates.append(heart_rate)
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e} in item: {datatype_content}")
            except KeyError:
                print(f"'HeartRate' key not found in: {datatype_content}")
            except (TypeError, ValueError) as e:
                print(f"Error in processing: {e} in item: {datatype_content}")
        elif datatype_content=="SPO2":
            try:
                SPO2 = int(item.get('value', None))
                SPO2_array.append(SPO2)
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e} in item: {datatype_content}")
            except KeyError:
                print(f"'SPO2' key not found in: {datatype_content}")
            except (TypeError, ValueError) as e:
                print(f"Error in processing: {e} in item: {datatype_content}")
        elif datatype_content == "Temperature":
            try:
                Temperature = int(item.get('value', None))
                Temprature_array.append(Temperature)
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e} in item: {datatype_content}")
            except KeyError:
                print(f"'Temperature' key not found in: {datatype_content}")
            except (TypeError, ValueError) as e:
                print(f"Error in processing: {e} in item: {datatype_content}")

    if heart_rates:
        min_heart_rate = heart_rates[0]
        max_heart_rate = heart_rates[0]
        sum_heart_rate = 0

        # Use for loop for calculations
        for rate in heart_rates:
            if rate < min_heart_rate:
                min_heart_rate = rate
            if rate > max_heart_rate:
                max_heart_rate = rate
            sum_heart_rate += rate
        avg_heart_rate = sum_heart_rate / len(heart_rates)

        print(f"Min Heart Rate: {min_heart_rate}, Max Heart Rate: {max_heart_rate}, Avg Heart Rate: {avg_heart_rate:.2f}")

        target_tabel.put_item(
            Item={
                'deviceid': DeviceId,
                'timestamp': datetime.now().isoformat(),
                'Data':"Heart",
                'min_rate': min_heart_rate,
                'max_rate': max_heart_rate,
                'avg_rate': int(avg_heart_rate),
                'Interval_Start_Time': config.app_config.StartTime,
                'Interval_End_Time': config.app_config.EndTime

            }
        )

    else:
        print("No Heart data found in the specified time range.")

    if SPO2_array:
        min_SPO2_rate = SPO2_array[0]
        max_SPO2_rate = SPO2_array[0]
        sum_SPO2_rate = 0

        # Use for loop for calculations
        for rate in SPO2_array:
            if rate < min_SPO2_rate:
                min_SPO2_rate = rate
            if rate > max_SPO2_rate:
                max_SPO2_rate = rate
            sum_SPO2_rate += rate
        avg_SPO2_rate = sum_SPO2_rate / len(SPO2_array)

        print(f"Min SPO2 Rate: {min_SPO2_rate}, Max SPO2 Rate: {max_SPO2_rate}, Avg SPO2 Rate: {avg_SPO2_rate:.2f}")

        target_tabel.put_item(
            Item={
                'deviceid': DeviceId,
                'timestamp': datetime.now().isoformat(),
                'Data': "SPO2",
                'min_rate': min_SPO2_rate,
                'max_rate': max_SPO2_rate,
                'avg_rate': int(avg_SPO2_rate),
                'Interval_Start_Time': config.app_config.StartTime,
                'Interval_End_Time': config.app_config.EndTime

            }
        )

    else:
        print("No SPO2 data found in the specified time range.")


    if Temprature_array:
        min_temp_rate = Temprature_array[0]
        max_temp_rate = Temprature_array[0]
        sum_temp_rate = 0

        # Use for loop for calculations
        for rate in Temprature_array:
            if rate < min_temp_rate:
                min_temp_rate = rate
            if rate > max_temp_rate:
                max_temp_rate = rate
            sum_temp_rate += rate
        avg_temp_rate = sum_temp_rate / len(Temprature_array)
        print(f"Min Temp Rate: {min_temp_rate}, Max Temp Rate: {max_temp_rate}, Avg Temp Rate: {avg_temp_rate:.2f}")

        target_tabel.put_item(
            Item={
                'deviceid': DeviceId,
                'timestamp': datetime.now().isoformat(),
                'Data': "Temperature",
                'min_rate': min_temp_rate,
                'max_rate': max_temp_rate,
                'avg_rate': int(avg_temp_rate),
                'Interval_Start_Time':config.app_config.StartTime,
                'Interval_End_Time':config.app_config.EndTime
            }
        )
    else:
        print("No Temp rate data found in the specified time range.")





