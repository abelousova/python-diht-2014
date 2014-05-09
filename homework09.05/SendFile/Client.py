import socket
import sys

HOST, PORT = "localhost", 9999
fileName = " ".join(sys.argv[1:])
with open(fileName) as f:
    data = f.read()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
finally:
    sock.close()

print("Sent:     {}".format(data))
print("Received: {}".format(received))