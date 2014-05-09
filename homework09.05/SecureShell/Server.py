# -*- coding: cp1251 -*-
import socket
import threading
import socketserver
import subprocess


isLoggedIn = {}
loginPassword = {}


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.commands = {'SignUp': self.signUp, 'LogIn': self.logIn, 'LogOut': self.logOut, 'Shell': self.shell}

    def signUp(self):
        login = self.data[1]
        password = self.data[2]
        if login in loginPassword.keys():
            self.request.sendall(bytes("Login already exists", "cp1251"))
            return
        loginPassword[login] = hash(password)
        isLoggedIn[self.client_address[0]] = True
        self.request.sendall(bytes("You've successfully signed up", "cp1251"))

    def logIn(self):
        login = self.data[1]
        password = self.data[2]
        if login not in loginPassword.keys() or hash(password) != loginPassword[login]:
            self.request.sendall(bytes("Invalid login and/or password", "cp1251"))
        else:
            isLoggedIn[self.client_address[0]] = True
            self.request.sendall(bytes("You've successfully logged in", "cp1251"))

    def logOut(self):
        isLoggedIn[self.client_address[0]] = False
        self.request.sendall(bytes("You've successfully logged out", "cp1251"))

    def shell(self):
        if not isLoggedIn[self.client_address[0]]:
            self.request.sendall(bytes("You must log in to execute shell commands", "cp1251"))
            return
        process = subprocess.Popen(self.data[1:], stdout=subprocess.PIPE)
        out, err = process.communicate()
        self.request.sendall(out)

    def handle(self):
        if self.client_address[0] not in isLoggedIn.keys():
            isLoggedIn[self.client_address[0]] = False

        while 1:
            try:
                self.data = str(self.request.recv(1024), 'utf-8').split()
                self.commands[self.data[0]]()
            except:
                break
            if len(self.data) == 0:
                break


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def client(ip, port, *messages):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        for message in messages:
            sock.sendall(bytes(message, 'utf-8'))
            response = str(sock.recv(1024), 'cp1251')
            print(response)
    finally:
        sock.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    client(ip, port, 'SignUp sashbel 1234', 'Shell ipconfig')
    #client(ip, port, 'Shell ping www.google.com')
    client(ip, port, 'LogOut', 'Shell ipconfig')
    client(ip, port, 'LogIn sashbel 1234', 'Shell ipconfig')

    server.shutdown()