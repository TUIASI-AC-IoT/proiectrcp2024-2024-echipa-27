
def create_connect_packet(client_id="test_client"):
    
    protocol_name = "MQTT"
    protocol_level = 0b00000101 
    connect_flags = 0b00000010  #doar clean start deocamdată
    keep_alive = 60  
    variable_header = (
        len(protocol_name).to_bytes(2, 'big') +
        protocol_name.encode() +
        protocol_level.to_bytes(1, 'big') +
        connect_flags.to_bytes(1, 'big') +
        keep_alive.to_bytes(2, 'big')
    )
    #print("variable_header",variable_header)

    payload = (
        len(client_id).to_bytes(2, 'big') +
        client_id.encode()
    )
    print("payload",payload)
    fixed_header = 0x10 
    remaining_length = len(variable_header) + len(payload)
    print("remaining_length",remaining_length)
    connect_packet = (
        fixed_header.to_bytes(1, 'big') +
        remaining_length.to_bytes(1, 'big') +
        variable_header +
        payload
        + b'\x05'+b'\x00\x00\x00\x00\x00'  # will, username, password
    )
    print("connect_packet",connect_packet)
    return connect_packet


def create_subscribe_packet(topic, qos=0, packet_id=1):
    packet_type = 0x82  # 0x1000 0010
    variable_header = packet_id.to_bytes(2, 'big')

    topic_encoded = len(topic).to_bytes(2, 'big') + topic.encode() + qos.to_bytes(1, 'big')
    payload = topic_encoded

    remaining_length = len(variable_header) + len(payload)

    subscribe_packet = (
        packet_type.to_bytes(1, 'big') +
        remaining_length.to_bytes(1, 'big') +
        variable_header +
        payload
    )
    print("subscribe_packet",subscribe_packet)
    return subscribe_packet