import json
import paho.mqtt.client as mqtt
import datetime
import time

HOST = "localhost"
PORT = 1883


class Light_Device():

    # setting up the intensity choices for Smart Light Bulb  
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"
        self.GotAck="FALSE"
        #Subscribe To commands
        self.client.subscribe("EDGE_COMMAND/#")
        #self.client.on_disconnect = self._on_disconnect

    def _register_device(self, device_id, room_type, device_type):
        message={}
        message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        message["device_id"] = device_id
        message["device_type"] = device_type
        message["device_room"]=room_type
        message["device_status"]="OFF"
        message["device_request"]="REGISTER_ME"

        print(f"---------->>>>>>>>>> DEVICE TO EDGE Device:{device_id} , Type:{device_type} , Room:{room_type} CMD:REGISTER_ME\n")
        time.sleep(1)
        self.client.publish("devices",json.dumps(message))

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        DeviceBrokerConnTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        Device_Id = self._device_id
        Device_Type = self._device_type
        Device_Room = self._room_type
        #print(f"Time:{DeviceBrokerConnTimeStamp}, DeviceId:{Device_Id},DeviceType:{Device_Type},DeviceRoom:{Device_Room} Connected to BROKER SERVICE with result code:{str(result_code)}")

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        item = {"topic": msg.topic, "payload": msg.payload, "timestamp": json.loads(msg.payload)["timestamp"]}
        data = json.loads(msg.payload)
        Edge_command = data["Edge_Command"]
        device_id=data["device_id"]
        Call_Reason=data["FilterBy"]

        device_type=data["FilterDevice"]
        device_room=data["FilterRoom"]

        if (Edge_command == "ACK_Registeration") and (self.GotAck=="FALSE"):
            device_reg_id = data["device_id"]
            device_type = data["device_type"]
            device_room = data["device_room"]
            Edge_Command = data["Edge_Command"]
            print(f"<<<<<<<-------------EDGE TO DEVICE Device:{device_reg_id} , Type:{device_type} , Room:{device_room} CMD:{Edge_Command}\n")
            self.GotAck="TRUE"

        elif (Edge_command == "GET_STATUS") and Call_Reason=="DEVICE_ID" and (device_id==self._device_id):
            #INCOMING MESSAGE DATA
            device_reg_id = self._device_id
            device_type = self._device_type
            device_room = self._room_type
            Edge_Command = data["Edge_Command"]
            print(f"<<<<<<<-------------EDGE TO DEVICE Device:{device_reg_id} , Type:{device_type} , Room:{device_room} CMD:{Edge_Command}\n")

            #Prepare OUTGOING MESSAGE DATA
            message = {}
            message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            message["device_id"] = self._device_id
            message["device_type"] = self._device_type
            message["device_room"] = self._room_type
            message["LIGHT_status"] = self._switch_status
            message["device_intensity"] = self._light_intensity
            message["device_request"] = "GET_STATUS_REPLY"
            Edge_Command = data["Edge_Command"]
            print(f"---------->>>>>>>>>> DEVICE TO EDGE Device:{self._device_id} , Type:{self._device_type} , Room:{self._room_type} CMD:{Edge_Command} REPLY\n")
            print(f"STATUS Device:{device_reg_id} , Type:{device_type} , Room:{device_room} ,SwitchState:{self._switch_status} Device Intensity:{self._light_intensity} CMD:{Edge_command} REPLY\n")
            time.sleep(1)
            self.client.publish("devices/#", json.dumps(message))

        elif (Edge_command == "GET_STATUS") and Call_Reason == "DEVICE_TYPE"  and (device_type == self._device_type):
            # INCOMING MESSAGE DATA
            device_reg_id = self._device_id
            device_type = self._device_type
            device_room = self._room_type
            Edge_Command = data["Edge_Command"]
            print(f"<<<<<<<-------------EDGE TO DEVICE Device:{device_reg_id} , Type:{device_type} , Room:{device_room} CMD:{Edge_Command}\n")

            # Prepare OUTGOING MESSAGE DATA
            message = {}
            message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            message["device_id"] = self._device_id
            message["device_type"] = self._device_type
            message["device_room"] = self._room_type
            message["LIGHT_status"] = self._switch_status
            message["device_intensity"] = self._light_intensity
            message["device_request"] = "GET_STATUS_REPLY"
            Edge_Command = data["Edge_Command"]
            print(f"---------->>>>>>>>>> DEVICE TO EDGE Device:{self._device_id} , Type:{self._device_type} , Room:{self._room_type} CMD:{Edge_Command} REPLY\n")
            print(f"STATUS Device:{device_reg_id} , Type:{device_type} , Room:{device_room} ,SwitchState:{self._switch_status} Device Intensity:{self._light_intensity} CMD:{Edge_command} REPLY\n")
            time.sleep(1)
            self.client.publish("devices/#", json.dumps(message))

        elif (Edge_command == "GET_STATUS") and Call_Reason == "ROOM" and (device_room == self._room_type):
            # INCOMING MESSAGE DATA
            device_reg_id = self._device_id
            device_type = self._device_type
            device_room = self._room_type
            Edge_Command = data["Edge_Command"]
            print(f"<<<<<<<-------------EDGE TO DEVICE Device:{device_reg_id} , Type:{device_type} , Room:{device_room} CMD:{Edge_Command}\n")

            # Prepare OUTGOING MESSAGE DATA
            message = {}
            message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            message["device_id"] = self._device_id
            message["device_type"] = self._device_type
            message["device_room"] = self._room_type
            message["LIGHT_status"] = self._switch_status
            message["device_intensity"] = self._light_intensity
            message["device_request"] = "GET_STATUS_REPLY"
            Edge_Command = data["Edge_Command"]
            print(
                f"---------->>>>>>>>>> DEVICE TO EDGE Device:{self._device_id} , Type:{self._device_type} , Room:{self._room_type} CMD:{Edge_Command} REPLY\n")
            print(
                f"STATUS Device:{device_reg_id} , Type:{device_type} , Room:{device_room} ,SwitchState:{self._switch_status} Device Intensity:{self._light_intensity} CMD:{Edge_command} REPLY\n")
            time.sleep(1)
            self.client.publish("devices/#", json.dumps(message))






    # Getting the current switch status of devices
    def _get_switch_status(self):
        pass

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        pass

    # Getting the light intensity for the devices
    def _get_light_intensity(self):
        pass

    # Setting the light intensity for devices
    def _set_light_intensity(self, light_intensity):
        pass    