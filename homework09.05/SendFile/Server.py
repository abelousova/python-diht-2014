import socketserver


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024).strip(), "utf-8")
        self.request.sendall(bytes(data.replace('bad', 'good'), "utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = socketserver.TCPServer((HOST, PORT), TCPHandler)

    server.serve_forever()