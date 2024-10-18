def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Conected")      
        client.subscribe("test/topic", qos=1)
        # trimite mesaj
        client.publish("test/topic", payload="Hello world", qos=1)
    else:
        print(f"Connect failed {rc}")