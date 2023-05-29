import paho.mqtt.client as mqtt
import time




def on_messege(client,userdata,message):
    print(f"Recive {message.payload.decode('utf-8')}")



mqtt_client = mqtt.Client("Server")
mqtt_client.connect("127.0.0.1", 1883, 69)

mqtt_client.loop_start()
mqtt_client.subscribe("#")
mqtt_client.on_message = on_messege
time.sleep(500)
mqtt_client.loop_stop()

