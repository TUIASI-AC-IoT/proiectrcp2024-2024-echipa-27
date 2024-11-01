
def create_connect_packet(client_id="test_client"):
    
    protocol_name = "MQTT"
    protocol_level = 0b00000101 
    connect_flags = 0b00000010  #doar clean start deocamdată
    keep_alive = 60  

    #
    # print(len(protocol_name).to_bytes(2, 'big')," protocol name",protocol_name.encode())
    
    # print(protocol_level.to_bytes(1, 'big'))
    # print(connect_flags.to_bytes(1, 'big'))
    # print(keep_alive.to_bytes(2, 'big'))

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
    packet_type = 0x10 
    remaining_length = len(variable_header) + len(payload)
    print("remaining_length",remaining_length)
    connect_packet = (
        packet_type.to_bytes(1, 'big') +
        remaining_length.to_bytes(1, 'big') +
        variable_header +
        payload
    )
    print("connect_packet",connect_packet)
    return connect_packet
