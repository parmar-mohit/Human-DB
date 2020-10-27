import os
from datetime import datetime
from socket import gethostbyname, gethostname
from threading import Thread

from Assets.Classes.User import User
from Assets.Server.ServerWindow import ServerWindow
from Assets.Server.server_start import server_start
from Assets.Server.sever_login import server_login
from Assets.write_log import write_log


def show_window(server_socket):
    while True:
        userLogin = server_login(server_socket)

        if not userLogin:
            serverSocket.close_all_connections()
            write_log("Connection with all clients Closed")
            serverSocket.close()
            write_log("Socket Closed")
            write_log("Closing Program,Exit Code 3")
            os._exit(3)

        write_log("admin User Logged In from Server Program")
        user = User(username="admin")
        user.update_login_date(datetime.now())
        serverWindow = ServerWindow(server_socket)
        exit = serverWindow.show_window()
        write_log("admin User Logged Out from Server Program")
        user.update_logout_date(datetime.now())
        if exit:
            serverSocket.close_all_connections()
            write_log("Connection with all clients Closed")
            serverSocket.close()
            write_log("Socket Closed")
            write_log("Closing Program,Exit Code 3")
            os._exit(3)


# clear contents of log.txt
fileWrite = open("log.txt", "w")
fileWrite.close()

write_log("Program Started")

serverSocket = server_start()
if serverSocket is None:
    write_log("Closing Program, Exit Code 2")
    exit(2)

serverSocket.listen()
write_log("Server Started,Listening at Address : (" + gethostbyname(gethostname()) + ",5432)")

Thread(target=show_window, args=(serverSocket,)).start()

serverSocket.accept_connections()
