import paho.mqtt.client as mqtt
import time

import random
import opcua as ua
import numpy as np

max_temperature = 40
min_temperature = 15

max_humidity = 70
max_pollution = 150
max_smoke = 1000

#opc_client=ua.Client('opc.tcp://127.0.0.1:4840')
#opc_client.connect()
#opc_client.get_node('ns=2;s="MS0"').get_child("2:Temperature").get_value()


mqtt_client = mqtt.Client("Temperature_in_Warehouses")
mqtt_client.connect("127.0.0.1", 1883, 69)

class Warehouse:
    
    def __init__(self, opc_address: str):
        self.name = None
        self.opc_client = ua.Client(opc_address)

    def connect(self):
        self.opc_client.connect()
        self.name = "warehouse" + str(self.opc_client.get_node("ns=2;i=1").get_value())
    
    

    def calc_avg_temperature(self):
        act_sum=0
        for i in range(5):
            act_sum += self.opc_client.get_node('ns=2;s="MS'+str(i)+'"').get_child("2:Temperature").get_value()
        
        return round(act_sum/5,2)

    def calc_avg_humidity(self):
        act_sum=0
        for i in range(5):
            act_sum += self.opc_client.get_node('ns=2;s="MS'+str(i)+'"').get_child("2:Humidity").get_value()
        
        return round(act_sum/5,2)

    def calc_avg_polution(self):
        act_sum=0
        for i in range(5):
            act_sum += self.opc_client.get_node('ns=2;s="MS'+str(i)+'"').get_child("2:AirPollution").get_value()
        
        return round(act_sum/5,2)

    def calc_max_smoke(self):
        act_max=0
        for i in range(5):
            act_smoke=self.opc_client.get_node('ns=2;s="MS'+str(i)+'"').get_child("2:Smoke").get_value()
            if act_max<act_smoke:
                act_max=act_smoke
        return act_max
    
    def mqtt_publish(self):
        act_avg_temperature=self.calc_avg_temperature()
        act_avg_humidity=self.calc_avg_humidity()
        act_avg_polution = self.calc_avg_polution()
        act_max_smoke = self.calc_max_smoke()

        mqtt_client.publish(self.name + "/avg_temperature", act_avg_temperature)
        mqtt_client.publish(self.name + "/avg_humidity", act_avg_humidity)
        mqtt_client.publish(self.name + "/avg_polution", act_avg_polution)
        mqtt_client.publish(self.name + "/max_smoke", act_max_smoke)
 
        
        if  act_avg_temperature > max_temperature:
            mqtt_client.publish(self.name + "/alarm", "Avg. temperature above max value")
            
        if  act_avg_temperature < min_temperature:
            mqtt_client.publish(self.name + "/alarm", "Avg. temperature bellow min value")
            
        if  act_avg_humidity > max_humidity:
            mqtt_client.publish(self.name + "/alarm", "Avg. humidity above max value, recommended dehumidifying procedure ")
            
        if  act_avg_polution > max_pollution:
            mqtt_client.publish(self.name + "/alarm", "Avg. air pollution above max value, recommended warehouse ventilation")
            
        if  act_max_smoke > max_smoke:
            mqtt_client.publish(self.name + "/alarm", "Detected smoke! Fire hazard!")
        
warehouses=[Warehouse('opc.tcp://127.0.0.1:4840'),
            Warehouse('opc.tcp://127.0.0.1:4841'),
            Warehouse('opc.tcp://127.0.0.1:4842'),
            Warehouse('opc.tcp://127.0.0.1:4843'),
            Warehouse('opc.tcp://127.0.0.1:4844')]
for warehouse in warehouses:
    warehouse.connect()
    
while True:
    for warehouse in warehouses:
        warehouse.mqtt_publish()
    time.sleep(1)
