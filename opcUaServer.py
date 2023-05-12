import time
import random
from opcua import Server

server = Server()
server.set_endpoint("opc.tcp://127.0.0.1:4840")
server.register_namespace("Room1")
objects=server.get_objects_node()
tempsens=objects.add_object('ns=2;s="TS1"', "Temperature Sensor 1")
tempsens.add_variable('ns=2;s="TS1_VendorName"',"TS1 Vendor Name","Sensor King")
temp = tempsens.add_variable('ns=2;s="TS1_Temperature"',"TS1 Temperature",20)
server.start()
try:
    while True:
        temperature = round(random.uniform(-1,1),2)
        temp.set_value(temperature)
        print("New temperature: "+str(temp.get_value()))
        time.sleep(2)

finally:
    server.stop()