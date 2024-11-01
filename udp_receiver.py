import socket
ip_addr = '127.0.0.1'
port = 5000

s_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_recv.bind ((ip_addr,port))

message, peer_addr = s_recv.recvfrom(512)

print('Received message: ', message.decode(),'>de la ',peer_addr)

s_recv.close()

