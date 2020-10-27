import os
from datetime import datetime

from Assets.Classes.ClientSocket import ClientSocket
from Assets.Client.ClientWindow import ClientWindow
from Assets.Client.client_login import client_login
from Assets.Client.client_start import client_start

clientSocket = ClientSocket()

if not client_start(clientSocket):
    os._exit(0)

request = 1
while True:
    valid, request, user = client_login(clientSocket, request)
    if not valid:
        clientSocket.close_connection()
        os._exit(0)

    user.loginDateTime = datetime.now()
    clientSocket.user_login(user, request)
    request += 1
    clientWindow = ClientWindow(clientSocket, user, request)
    request, quit = clientWindow.show_window()
    if quit:
        clientSocket.close_connection()
        os._exit(0)
