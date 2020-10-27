from socket import socket, timeout
from threading import Thread
from time import sleep

from Assets.Classes.ClientConnection import ClientConnection
from Assets.write_log import write_log


class ServerSocket(socket):
    def __init__(self):
        super().__init__()
        self.settimeout(7)

        self.acceptConnection = True
        self.connected = {}  # address as key and clientConnection object as value

    def accept_connections(self):
        while True:
            if self.acceptConnection:
                try:
                    client, addr = self.accept()
                    write_log("Connected to Client with IP : " + str(addr))
                    client.settimeout(7)
                    clientConnection = ClientConnection(client, addr, self)
                    Thread(target=clientConnection.run).start()
                    self.connected[str(addr)] = clientConnection
                except timeout:
                    pass
                except:
                    break
            else:
                sleep(7)

    def close_all_connections(self):
        clientList = self.connected.values()
        for client in clientList:
            client.close_connection(True)
