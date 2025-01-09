
# def create_connect_packet(client_id="test_client"):
    
#     protocol_name = "MQTT"
#     protocol_level = 0b00000101 
#     connect_flags = 0b00000010  #doar clean start deocamdată
#     keep_alive = 60  
#     variable_header = (
#         len(protocol_name).to_bytes(2, 'big') +
#         protocol_name.encode() +
#         protocol_level.to_bytes(1, 'big') +
#         connect_flags.to_bytes(1, 'big') +
#         keep_alive.to_bytes(2, 'big')+
#         b'\x00'
#     )
#     #print("variable_header",variable_header)

#     payload = (
#         len(client_id).to_bytes(2, 'big') +
#         client_id.encode()
#     )
#     print("payload",payload)
#     fixed_header = 0x10 
#     remaining_length = len(variable_header) + len(payload)
#     print("remaining_length",remaining_length)
    

#     connect_packet = (
#         fixed_header.to_bytes(1, 'big') +
#         remaining_length.to_bytes(1, 'big') +
#         variable_header +
#         payload
#     )
#     print("connect_packet",connect_packet)
#     return connect_packet

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
    # Fixed header
    packet_type = 0x30  # PUBLISH
    dup_flag = 0x00
    qos_flag = (qos & 0x03) << 1
    retain_flag = 0x00
    fixed_header = packet_type | dup_flag | qos_flag | retain_flag

    # Variable header
    topic_length = len(topic).to_bytes(2, 'big')
    variable_header = topic_length + topic.encode()
    
    # Add packet ID for QoS > 0
    if qos > 0:
        variable_header += packet_id.to_bytes(2, 'big')
    
    # Payload
    payload = message.encode()
    
    # Calculate remaining length
    remaining_length = len(variable_header) + len(payload)
    
    return (
        fixed_header.to_bytes(1, 'big') +
        remaining_length.to_bytes(1, 'big') +
        variable_header +
        payload
    )

def create_subscribe_packet(topic, qos=0, packet_id=1):
    # Fixed header
    packet_type = 0x82  # SUBSCRIBE command
    
    # Variable header
    variable_header = (
        packet_id.to_bytes(2, 'big') +  # Packet ID
        b'\x00'  # Properties length = 0
    )
    
    # Payload (Topic Filter + Subscription Options)
    topic_length = len(topic).to_bytes(2, 'big')
    subscription_options = qos & 0x03  # QoS bits
    payload = topic_length + topic.encode() + subscription_options.to_bytes(1, 'big')
    
    # Calculate remaining length
    remaining_length = len(variable_header) + len(payload)
    
    return (
        packet_type.to_bytes(1, 'big') +
        remaining_length.to_bytes(1, 'big') +
        variable_header +
        payload
    )

def create_unsubscribe_packet(topic, packet_id=1):
    packet_type = 0xA2
    variable_header = packet_id.to_bytes(2, 'big')
    payload = len(topic).to_bytes(2, 'big') + topic.encode()
    remaining_length = len(variable_header) + len(payload)
    
    return (
        packet_type.to_bytes(1, 'big') +
        remaining_length.to_bytes(1, 'big') +
        variable_header +
        payload
    )

def create_pingreq_packet():
    return b'\xC0\x00'

def create_connect_packet_with_auth(client_id, username=None, password=None, will_topic=None, will_message=None, clean_session=True):
    protocol_name = "MQTT"
    protocol_level = 0b00000101
    # Set connect flags
    connect_flags = 0b00000000
    if clean_session:
        connect_flags |= 0b00000010
    if username:
        connect_flags |= 0b10000000
    if password:
        connect_flags |= 0b01000000
    if will_topic and will_message:
        connect_flags |= 0b00000100
    
    keep_alive = 60
    
    variable_header = (
        len(protocol_name).to_bytes(2, 'big') +
        protocol_name.encode() +
        protocol_level.to_bytes(1, 'big') +
        connect_flags.to_bytes(1, 'big') +
        keep_alive.to_bytes(2, 'big') +
        b'\x00'
    )
    
    # Build payload
    payload = bytearray(len(client_id).to_bytes(2, 'big') + client_id.encode())
    
    if will_topic and will_message:
        payload.extend(len(will_topic).to_bytes(2, 'big') + will_topic.encode())
        payload.extend(len(will_message).to_bytes(2, 'big') + will_message.encode())
    
    if username:
        payload.extend(len(username).to_bytes(2, 'big') + username.encode())
    
    if password:
        payload.extend(len(password).to_bytes(2, 'big') + password.encode())
    
    fixed_header = 0x10
    remaining_length = len(variable_header) + len(payload)
    
    return (
        fixed_header.to_bytes(1, 'big') +
        remaining_length.to_bytes(1, 'big') +
        variable_header +
        bytes(payload)
    )