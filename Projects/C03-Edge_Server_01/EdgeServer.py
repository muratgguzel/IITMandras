import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883
WAIT_TIME = 0.25
import datetime


class Edge_Server:

    def __init__(self, instance_name):
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        # Edge server subscribes a topic of devices
        self.client.subscribe("devices/#")
        self._registered_list = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.
    def _on_connect(self, client, userdata, flags, result_code):
        EdgeServerBrokerConnTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        print(
            f"Time:{EdgeServerBrokerConnTimeStamp}, Edge Server Connected to BROKER SERVICE with result code:{str(result_code)}")
        client.subscribe("devices/#")
        print("Time:Edge Server Subscribed To Topic devices\n")

    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        item = {"topic": msg.topic, "payload": msg.payload, "timestamp": json.loads(msg.payload)["timestamp"]}
        data = json.loads(msg.payload)
        self._registered_list.append(data["device_id"])
        device_reg_id = data["device_id"]
        device_type = data["device_type"]
        device_room = data["device_room"]
        device_request = data["device_request"]

        # Sense the topic
        if (device_request == "REGISTER_ME"):
            message = {}
            message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            message["device_id"] = device_reg_id
            message["device_type"] = device_type
            message["device_room"] = device_room
            message["Edge_Command"] = "ACK_Registeration"
            self.client.publish("EDGE_COMMAND", json.dumps(message), qos=0)
            print(f"Device:{device_reg_id} , Type:{device_type} , Room:{device_room} registered\n")

        elif (device_request == "GET_STATUS_REPLY") and (device_type=="LIGHT"):
            device_intensity=data["device_intensity"];
            device_status=data["device_status"];
            print(f"STATUS Device:{device_reg_id} , Type:{device_type} , Room:{device_room} ,SwitchState:{device_status} Device Intensity:{device_intensity} CMD:{device_request} REPLY\n")

        elif (device_request == "GET_STATUS_REPLY") and (device_type == "AC"):
            device_status=data["device_status"]
            device_room_temp=data["device_room_temp"]
            print(f"STATUS Device:{device_reg_id} , Type:{device_type} , Room:{device_room},Room_Temp:{device_room_temp} ,SwitchState:{device_status}  CMD:{device_request} REPLY\n")


    # Returning the current registered list
    def get_registered_device_list(self):
        while len(self._registered_list)<8 :
            time.sleep(5)
        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self):
        message = {}
        message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        message["Edge_Command"] = "GET_STATUS"
        self.client.publish("EDGE_COMMAND", json.dumps(message), qos=0)

    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self):
        pass