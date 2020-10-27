from socket import gethostname, gethostbyname
from tkinter import ttk, messagebox

from PIL import Image, ImageTk
from ttkthemes import ThemedTk

from Assets.Classes.ServerSocket import ServerSocket
from Assets.write_log import write_log


# server_start function shows a window on screen with a button asking to start server
# if user clicks on button a socket is created and it is binded to certain server address
# and the newly created socket is returned else None is returned is user closes window
def server_start():
    def server_start_button_on_click():
        nonlocal ipAddr, mainWin, serverSocket
        serverAddress = (ipAddr, 5432)
        serverSocket = ServerSocket()
        try:
            serverSocket.bind(serverAddress)
            write_log("Socket Created")
        except Exception as error:
            messagebox.showerror("Server Error", "Error : " + str(
                error) + "\nThere was a problem Starting Server.Restarting program might fix the problem")
            write_log("Error : " + str(error))
            write_log("Closing Program, Exit Code 1")
            exit(1)
        else:
            mainWin.destroy()

    ipAddr = gethostbyname(gethostname())
    serverSocket = None

    mainWin = ThemedTk(theme="breeze")
    mainWin.title("Human DB")
    mainWin.iconbitmap("Images/iconbitmap.ico")
    mainWin.resizable(False, False)

    logoImage = Image.open("Images/logo.png")
    logoImage = ImageTk.PhotoImage(logoImage.resize((75, 75), Image.ANTIALIAS))

    ttk.Label(mainWin, image=logoImage).grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(mainWin, text="Human DB", font=("Helvetica", 22)).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(mainWin, text="Start Server at IP : " + ipAddr, command=server_start_button_on_click).grid(row=1,
                                                                                                          column=0,
                                                                                                          columnspan=2,
                                                                                                          padx=5,
                                                                                                          pady=5)

    mainWin.mainloop()

    return serverSocket
