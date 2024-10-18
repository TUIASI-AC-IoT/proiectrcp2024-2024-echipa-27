import paho.mqtt.client as mqtt
from on_connect import on_connect
from on_message import on_message
from on_publish import on_publish
from on_subscribe import on_subscribe
from on_disconnect import on_disconnect

# Create a client instance
client = mqtt.Client(protocol=mqtt.MQTTv5)


client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect


client.connect("broker.hivemq.com", 1883, 60)

client.loop_start()

import time
time.sleep(10)

client.loop_stop()
client.disconnect()