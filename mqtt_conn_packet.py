
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
        keep_alive.to_bytes(2, 'big')+
        b'\x00'
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
    )
    print("connect_packet",connect_packet)
    return connect_packet

def encode_variable_byte_integer(value):
    encoded_bytes = bytearray()
    while True:
        digit = value % 128
        value = value // 128
        if value > 0:
            digit |= 0x80
        encoded_bytes.append(digit)
        if value == 0:
            break
    return bytes(encoded_bytes)

def create_publish_packet(topic, message, qos=0, packet_id=1):
    fixed_header = 0x30  # 00110000 for PUBLISH
    if qos == 1:
        fixed_header |= 0x02  # Set QoS to 1
    elif qos == 2:
        fixed_header |= 0x04  # Set QoS to 2

    topic_encoded = len(topic).to_bytes(2, 'big') + topic.encode()
    variable_header = topic_encoded
    if qos > 0:
        variable_header += packet_id.to_bytes(2, 'big')
    payload = message.encode()
    print('payload for publish packet', payload)
    remaining_length = len(variable_header) + len(payload)
    
    publish_packet = (
        fixed_header.to_bytes(1, 'big') +
        encode_variable_byte_integer(remaining_length) +
        variable_header +
        payload
    )
    
    print("publish_packet", publish_packet)
    return publish_packet

def create_subscribe_packet(topic, qos=0, packet_id=1):
    packet_type = 0x82  #fixed head
    
    variable_header = (
        b'\x05\xbe' +  # pachet identifier
        b'\x00'   # pachet length
    )
    topic_encoded = len(topic).to_bytes(2, 'big') + topic.encode() + qos.to_bytes(1, 'big')
    payload = topic_encoded
    remaining_length = len(variable_header) + len(payload)
    print("remaining_length:", remaining_length)
    subscribe_packet = (
        packet_type.to_bytes(1, 'big') +
        remaining_length.to_bytes(1, 'big') +  
        variable_header +  
        payload  
    )

    print("subscribe_packet:", subscribe_packet)
    return subscribe_packet