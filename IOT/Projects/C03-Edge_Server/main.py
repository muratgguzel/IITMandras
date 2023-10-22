import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 1.5

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

print("EDGE SERVER INITIATION \n" )
edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)

#print("EDGE SERVER INITIATION COMPLETED AND CONNECTED TO BROKER\n" )


#print("REGISTRATION OF LIGHT DEVICES INITIATED \n" )

#print("\nREGISTERING LIGHT 1 IN KITCHEN")
#light_device_1 = Light_Device("light_1", "Kitchen")
#time.sleep(WAIT_TIME)

#print("\nREGISTERING LIGHT 2 IN GARAGE")
#light_device_2 = Light_Device("light_2", "Garage")
#time.sleep(WAIT_TIME)

#print("\nREGISTERING LIGHT 3 IN BEDROOM")
#light_device_3 = Light_Device("light_3", "Bed Room1")
#time.sleep(WAIT_TIME)

#print("\nREGISTERING LIGHT 4 IN BEDROOM2")
#light_device_4 = Light_Device("light_4", "Bed Room2")
#time.sleep(WAIT_TIME)

#print("\nREGISTERING LIGHT 5 IN LIVING ROOM")
#light_device_5 = Light_Device("light_5", "Living Room")
#time.sleep(WAIT_TIME)

##print("REGISTRATION OF AC DEVICES INITIATED \n" )

#print("\nREGISTERING AC1 IN BED ROOM 1")
#ac_device_1 = AC_Device("ac_1", "BR1")
#time.sleep(WAIT_TIME)

#print("\nREGISTERING AC2 IN LIVING ROOM 1")
#ac_device_2 = AC_Device("ac_2", "Living Room")
#time.sleep(WAIT_TIME)

#print("\nREGISTERING AC3 IN LIVING ROOM 3")
#ac_device_3 = AC_Device("ac_3", "Living Room")
#time.sleep(WAIT_TIME)


registered_device_list=edge_server_1.get_registered_device_list()
print("ALL DEVICES REGISTERED SUCCESSFULLY REGISTERED IDS:\n\n", registered_device_list)
time.sleep(WAIT_TIME)

print("\n\nSTARTING TO GET ALL DEVICES STATUS BY DEVICE ID")
BY_DEVICE_ID="DEVICE_ID"
edge_server_1.get_status(BY_DEVICE_ID)


print("\n\nSTARTING TO GET ALL DEVICES STATUS BY DEVICE TYPE AS LIGHT")
BY_DEVICE_TYPE="DEVICE_TYPE"
FLAG_DEVICE_TYPE="LIGHT"
edge_server_1.get_status(BY_DEVICE_TYPE,FLAG_DEVICE_TYPE)


print("\nSTARTING TO GET ALL DEVICES STATUS BY DEVICE TYPE AS AC")
BY_DEVICE_TYPE="DEVICE_TYPE"
FLAG_DEVICE_TYPE="AC"
edge_server_1.get_status(BY_DEVICE_TYPE,FLAG_DEVICE_TYPE)


#print("\nSTARTING TO GET ALL DEVICES STATUS BY DEVICE TYPE")
#BY_DEVICE_TYPE="ROOM_TYPE"
#edge_server_1.get_status(BY_DEVICE_TYPE)

#print("\nSTARTING TO GET ALL DEVICES STATUS BY DEVICE TYPE")
#BY_DEVICE_TYPE="ALL"
#edge_server_1.get_status(BY_DEVICE_TYPE)





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
