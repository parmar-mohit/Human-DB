import os
from pickle import loads
from socket import socket, timeout
from threading import Thread
from time import sleep
from tkinter import messagebox

from Assets.Classes.Message import Message
from Assets.clientAction import clientAction


class ClientSocket(socket):
    def __init__(self):
        super().__init__()
        self.settimeout(7)
        self.messages = []

    def add_attendance(self, course, year, series, request):
        message = Message("order", 10, (course, year, series), request)
        self.send(message.encode())

    def add_new_user(self, user, request: int):
        message = Message("order", 3, user, request)
        self.send(message.encode())

    def add_student(self, student, request):
        message = Message("request", 7, student, request)
        self.send(message.encode())

        return self.get_message(request).info

    def change_password(self, username, password, request):
        message = Message("order", 5, (username, password), request)
        self.send(message.encode())

    def close_connection(self):
        message = Message("order", 1, None, None)
        self.send(message.encode())

    def connect_server(self, ip):
        try:
            self.connect((ip, 5432))
            Thread(target=self.recieve_messages).start()
        except:
            return False
        return True

    def delete_student(self, sid, course, year, request):
        message = Message("order", 9, (sid, course, year), request)
        self.send(message.encode())

    def get_message(self, request: int):
        while True:
            for message in self.messages:
                if message.request == request:
                    self.messages.remove(message)
                    return message
            sleep(2)

    def recieve_messages(self):
        while True:
            try:
                recvMessage = b""
                while True:
                    try:
                        receivedData = self.recv(4096)
                        if not receivedData: break
                        recvMessage += receivedData
                    except timeout:
                        break
                    except ConnectionResetError:
                        messagebox.showerror("Connection Error", "Connection was closed by server")
                        self.close()
                        os._exit(0)

                if len(recvMessage) == 0:
                    continue

                recvMessage = loads(recvMessage)

                if recvMessage.action in clientAction:
                    clientAction[recvMessage.action](recvMessage, self)
                else:
                    self.messages.append(recvMessage)
            except OSError:
                break

    def request_attendance_dataframe(self, course, year, request):
        message = Message("request", 11, (course, year), request)
        self.send(message.encode())

        return self.get_message(request).info

    def request_course_dataframe(self, request):
        message = Message("request", 6, None, request)
        self.send(message.encode())

        return self.get_message(request).info

    def request_user_dataframe(self, request: int):
        message = Message("request", 2, None, request)
        self.send(message.encode())

        return self.get_message(request).info

    def student_dataframe(self, coursename, year, request):
        message = Message("request", 8, (coursename, year), request)
        self.send(message.encode())

        return self.get_message(request).info

    def user_login(self, user, request: int):
        message = Message("order", 4, user, request)
        self.send(message.encode())
