import socket

my_ip_addr = '127.0.0.1'
my_port = 5005

peer_ip_addr = '127.0.0.1'
peer_port = 5000

s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_send.bind((my_ip_addr, my_port))

s_send.sendto(b'Hello, peer!', (peer_ip_addr, peer_port))