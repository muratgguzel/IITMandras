
import json
import paho.mqtt.client as mqtt
import datetime

HOST = "localhost"
PORT = 1883
    
class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32  

    def __init__(self, device_id, room):
        
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._switch_status = "OFF"
        self.client.subscribe("EDGE_COMMAND_ACK/#")
        self.GotAck = "FALSE"
        # self.client.on_disconnect = self._on_disconnect
    # calling registration method to register the device
        self._register_device(self._device_id, self._room_type, self._device_type)
    def _register_device(self, device_id, room_type, device_type):
        message = {}
        message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        message["device_id"] = device_id
        message["device_type"] = device_type
        message["device_room"] = room_type
        message["device_status"] = "OFF"
        message["device_request"]="REGISTER_ME"
        self.client.publish("devices", json.dumps(message))
        print(f"---------->>>>>>>>>> DEVICE TO EDGE Device:{device_id} , Type:{device_type} , Room:{room_type} CMD:REGISTER_ME\n")

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        DeviceBrokerConnTimeStamp=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        Device_Id=self._device_id
        Device_Type=self._device_type
        Device_Room=self._room_type

        #print(f"Time:{DeviceBrokerConnTimeStamp}, DeviceId:{Device_Id},DeviceType:{Device_Type},DeviceRoom:{Device_Room} Connected to BROKER SERVICE with result code:{str(result_code)}")

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        item = {"topic": msg.topic, "payload": msg.payload, "timestamp": json.loads(msg.payload)["timestamp"]}
        data = json.loads(msg.payload)
        Edge_command=data["Edge_Command"]

        if (Edge_command=="ACK_Registeration") and (self.GotAck=="FALSE"):
            device_reg_id = data["device_id"]
            device_type = data["device_type"]
            device_room = data["device_room"]
            Edge_Command = data["Edge_Command"]
            print(f"<<<<<<<-------------EDGE TO DEVICE Device:{device_reg_id} , Type:{device_type} , Room:{device_room} CMD:REGISTER_ACK\n")
            self.GotAck="TRUE"


    # Getting the current switch status of devices 
    def _get_switch_status(self):
        pass

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        pass

    # Getting the temperature for the devices
    def _get_temperature(self):
        pass        

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        pass
    
