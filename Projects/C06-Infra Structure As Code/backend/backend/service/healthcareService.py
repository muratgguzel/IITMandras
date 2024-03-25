from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS
import boto3

# A very basic API created using Flask that has two possible routes for requests.

app = Flask(__name__)
CORS(app)

#Create Dynamodb client using boto3
dynamo_client = boto3.client(
    'dynamodb',
    region_name='us-east-1'
)

# The service basepath has a short response just to ensure that healthchecks
# sent to the service root will receive a healthy response.
@app.route("/api/")
def healthCheckResponse():
    return jsonify({"message" : "Nothing here, used for health check. Try /api/raw-data instead."})

# Get request for raw-data
@app.route("/api/raw-data")
def getRawData():

    # read the request args to get deviceid, startdate and enddate
    deviceid = request.args.get('deviceid')
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')

    #Query dynamodb
    response = dynamo_client.query(
        TableName='HealthcareData',
        KeyConditionExpression='deviceid = :deviceid AND #ts BETWEEN :startdate AND :enddate',
        ExpressionAttributeValues={
            ':deviceid': {'S': deviceid},
            ':startdate': {'S': startdate},
            ':enddate': {'S': enddate}
        },
        ExpressionAttributeNames={
        "#ts": "timestamp"
        }
    )
    return jsonify(response['Items'])

# Run the service on the local server it has been deployed to,
# listening on port 8080.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
