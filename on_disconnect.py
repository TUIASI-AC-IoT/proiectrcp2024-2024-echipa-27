def on_disconnect(client, userdata, rc, properties=None):
    print(f"Disconnected with result code {rc}")