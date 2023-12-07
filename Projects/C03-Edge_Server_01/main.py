import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 10

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)

registered_device_list=edge_server_1.get_registered_device_list()
print("All devices registered successfully. Registered device IDs:", registered_device_list)



edge_server_1.get_status()

#print("\nRegistering To Light 1")
#light_device_1 = Light_Device("light_1", "Kitchen")
#time.sleep(WAIT_TIME)
#print("\nRegistering To Light 2")
#light_device_2 = Light_Device("light_2", "Garage")
#time.sleep(WAIT_TIME)
#print("\nRegistering To Light 3")
#light_device_3 = Light_Device("light_3", "Bed Room1")
#time.sleep(WAIT_TIME)
#print("\nRegistering To Light 4")
#light_device_4 = Light_Device("light_4", "Bed Room2")
#time.sleep(WAIT_TIME)
#print("\nRegistering To Light 5")
#light_device_5 = Light_Device("light_5", "Living Room")
#time.sleep(WAIT_TIME)

#print("\nRegistering To AC 1")
#ac_device_1 = AC_Device("ac_1", "BR1")
#time.sleep(WAIT_TIME)

#print("\nRegistering To AC 2")
#ac_device_2 = AC_Device("ac_2", "Living Room")
#time.sleep(WAIT_TIME)

#print("\nRegistering To AC 3")
#ac_device_3 = AC_Device("ac_3", "Living Room")
#time.sleep(WAIT_TIME)



while True:
    try:
        time.sleep(0.5)
    #Disconnect the client from MQTT broker and stop the loop gracefully at
    # Keyboard interrupt (Ctrl+C)
    except KeyboardInterrupt:
        #edge_server_1.client.disconnect()
        #edge_server_1.client.loop_stop()
        break


# Creating the ac_device  
#print("\nCreating the AC devices for their respective rooms. ")
#ac_device_1 = AC_Device("ac_1", "BR1")
#time.sleep(WAIT_TIME)

#print("\nSmart Home Simulation stopped.")
#edge_server_1.terminate()
