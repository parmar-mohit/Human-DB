import os
from tkinter import messagebox


def close_connection(message, socket):
    socket.close()
    messagebox.showerror("Connection Error", "Connection was closed by server")
    os._exit(0)


clientAction = {
    1: close_connection
}
