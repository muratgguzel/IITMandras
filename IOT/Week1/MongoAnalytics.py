import pymongo
import json

#Reading the configuration file
f=open("configanalytics.json")
config = json.loads(f.read())
f.close()

#Initializing connection to the database
dbclient = pymongo.MongoClient(config["db_host"], config["db_port"])
db = dbclient[config["db_name"]]
dbt = db[config["db_collection"]]

#Querying for the messages that were published to the `devices/temp` topic, on 01 Jan 2021
entries = dbt.find({"topic":"devices/temp", \
                    "timestamp":  {"$gte": "2023-10-07T14:00:00.000Z", \
                                   "$lt" : "2023-10-07T14:30:00.000Z"}})

#Print the entries
for entry in entries:
    print(entry)