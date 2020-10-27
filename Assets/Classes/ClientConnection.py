from pickle import loads
from socket import timeout
from threading import Thread

from Assets.Classes.Message import Message
from Assets.serverAction import serverAction
from Assets.write_log import write_log


class ClientConnection:
    def __init__(self, socket, addr, server_socket):
        self.socket = socket
        self.addr = addr
        self.serverSocket = server_socket
        self.user = None
        self.accept = True

    def close_connection(self, send_message: bool = False):
        if send_message:
            message = Message("order", 1, None, None)
            self.socket.send(message.encode())

        self.serverSocket.connected = {key: val for key, val in self.serverSocket.connected.items() if
                                       key != str(self.addr)}
        self.socket.close()
        if self.user is None:
            write_log("Connection closed with client at IP : " + str(self.addr))
        else:
            write_log("Connection Closed with " + self.user.username + " client at IP : " + str(self.addr))

    def receive_message(self):
        while True:
            try:
                recvMessage = b""
                while True:
                    try:
                        receivedData = self.socket.recv(4096)
                        if len(receivedData) == 0:
                            break
                        recvMessage += receivedData
                    except timeout:
                        break

                if len(recvMessage) == 0:
                    continue

                recvMessage = loads(recvMessage)
                return recvMessage
            except OSError:
                self.close_connection()
                break

    def run(self):
        while self.serverSocket.acceptConnection:
            message = self.receive_message()
            if message is None:
                break
            else:
                Thread(target=serverAction[message.action], args=(message, self)).start()
