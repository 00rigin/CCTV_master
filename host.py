import socket


s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))
netAddress=s.getsockname()[0]

print(netAddress)
