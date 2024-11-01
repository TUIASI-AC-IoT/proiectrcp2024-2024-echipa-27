
import socket
from mqtt_conn_packet import create_connect_packet 

BROKER_HOST = "broker.hivemq.com"
BROKER_PORT = 1883
print("Conectare la brokerul MQTT:", BROKER_HOST, "pe portul", BROKER_PORT)
def connect_to_broker():
    try:
            #initializare sockett
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((BROKER_HOST, BROKER_PORT))
        

        # Trimiterea pachetului
        client_id = "test_client"
        client_socket.sendall(create_connect_packet(client_id))
        print("CONNECT trimis")

        # primire connack
        connack_packet = client_socket.recv(4)
        print(connack_packet)
        packet_type = connack_packet[0] >> 4
        print("Tip pachet:", packet_type)
        if packet_type == 2:  #if connack
            print("connack primit")
            print("success")
        else:
            print("nu am primit connack")
        client_socket.close()
        print("exit")
        exit(1)
    except Exception as e:
        print("error", e)
        exit(0)

if __name__ == "__main__":
    connect_to_broker()
