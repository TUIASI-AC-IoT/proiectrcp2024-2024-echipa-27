import socket
from mqtt_conn_packet import create_connect_packet, create_publish_packet, create_subscribe_packet

BROKER_HOST = 'broker.hivemq.com'
BROKER_PORT = 1883

def connect_to_broker():
    try:
        # Initializare socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((BROKER_HOST, BROKER_PORT))

        # Trimiterea pachetului CONNECT
        client_id = "test_client"
        client_socket.sendall(create_connect_packet(client_id))
        print("CONNECT trimis")

        # Primire pachet CONNACK
        connack_packet = client_socket.recv(4)
        print("connack_packet:", connack_packet)
        packet_type = connack_packet[0] >> 4
        print("Tip pachet:", packet_type)
        if packet_type == 2:  # Verificăm dacă este CONNACK
            print("CONNACK primit")
            print("Conectare reușită")
            return client_socket
        else:
            print("Nu s-a primit un pachet CONNACK valid")
            client_socket.close()
            return None
    except Exception as e:
        print("Eroare la conectarea la broker:", e)
        return None


def subscribe_topic(broker_socket, topic):
    try:
        subscribe_packet = create_subscribe_packet(topic)
        broker_socket.sendall(subscribe_packet)
        print(f"Solicitare de abonare trimisă pentru topicul '{topic}'.")
        suback_packet = broker_socket.recv(5)
        print("suback_packet:", suback_packet)
        if len(suback_packet) < 5:
            print("Pachet SUBACK incomplet primit.")
            return False
        packet_type = suback_packet[0] >> 4
        print("Tip pachet suback:", packet_type)
        if packet_type != 9:
            print("Pachet SUBACK invalid.")
            return False
        return_code = suback_packet[4]
        print('return_code',return_code)
        if return_code == 0x80:
            print("abonarea a fost refuzată.")
            return False
        else:
            print("Abonare reușită")
            return True
    except Exception as e:
        print(f"Eroare la abonare: {e}")
        return False


def main():
    host = BROKER_HOST
    port = BROKER_PORT
    client_id = 'test_client'

    broker_socket = connect_to_broker()
    if broker_socket is None:
        return
    subscribed = subscribe_topic(broker_socket, 'senzor/temperatura/living')
    if not subscribed:
        broker_socket.close()
        return
    broker_socket.close()

if __name__ == "__main__":
    main()
