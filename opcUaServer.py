import time
import random
import opcua as ua
import numpy as np
import argparse


def opc_server(port, id):
    opc_url="opc.tcp://127.0.0.1:" + str(port)

    server = ua.Server()
    server.set_endpoint(opc_url)

    server.register_namespace("Warehouse "+str(id))
    objects=server.get_objects_node()
    objects.add_variable(2,'Warehouse ID',id)
    stations=[]
    for i in range(5):
        stations.append(objects.add_object('ns=2;s="MS'+str(i)+'"', "Measuring station " + str(i)))
        stations[i].add_variable(2,'Temperature',round(np.random.normal(25,3,1)[0],2))
        stations[i].add_variable(2,'Humidity',round(np.random.normal(50,5,1)[0],2))
        stations[i].add_variable(2,'AirPollution',round(np.random.normal(100,20,1)[0],2))
        stations[i].add_variable(2,'Smoke',round(np.random.normal(5,10,1)[0],2))

    server.start()
    print(f"Server started on port: {port} for warehouse {id}")
    try:
        while True:
            for i in range(5):
                stations[i].get_child("2:Temperature").set_value(round(np.random.normal(25,3,1)[0],2))
                stations[i].get_child("2:Humidity").set_value(round(np.random.normal(50,5,1)[0],2))
                stations[i].get_child("2:AirPollution").set_value(round(np.random.normal(100,20,1)[0],2))
                stations[i].get_child("2:Smoke").set_value(round(np.random.normal(700,100,1)[0],2))
            #temperature = round(random.uniform(-1,1),2)
            #temp.set_value(temperature)
            #print("New temperature: "+str(temp.get_value()))
            print("Updated values")
            time.sleep(2)

    finally:
        server.stop()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Opcua server")
    
    parser.add_argument("--port", type=int, default=4840, help="Port of the server")
    parser.add_argument("--id", type=int, default=0, help="Id of the warehouse")
    
    args = parser.parse_args()
    opc_server(args.port, args.id)