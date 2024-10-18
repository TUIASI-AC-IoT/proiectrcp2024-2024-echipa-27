def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed: {mid} QoS: {granted_qos}")