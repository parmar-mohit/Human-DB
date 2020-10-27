import os
from tkinter import ttk, messagebox

from PIL import ImageTk, Image
from ttkthemes import ThemedTk

from Assets.Classes.ClientSocket import ClientSocket
from Assets.check_ip import check_ip


def client_start(client_socket: ClientSocket) -> bool:  # basic server start function
    def ipConnectButtonOnClick():
        nonlocal ip

        ipFrame.grid_forget()
        statusLabel.config(text="Connecting to server")
        val = client_socket.connect_server(ip)
        if val:
            nonlocal connected
            connected = True
            mainWin.quit()
        else:
            messagebox.showerror("Connection Error", "Can't Connect to server\nCheck your IP or try Again")
            ipFrame.grid(row=1, column=0, padx=5, pady=5)
            statusLabel.config(text="")

    def connectButtonOnClick():
        ip = ipEntry.get()
        ipEntry.delete(0, "end")

        if check_ip(ip) == True:
            ipFrame.grid_forget()
            statusLabel.config(text="Connecting to server")
            val = client_socket.connect_server(ip)
            if val:
                nonlocal connected
                connected = True
                fileWrite = open("server.IP", "w")
                fileWrite.write(ip)
                fileWrite.close()
                mainWin.quit()
            else:
                messagebox.showerror("Connection Error", "Can't Connect to server\nCheck your IP or try Again")
                ipFrame.grid(row=1, column=0, padx=5, pady=5)
                statusLabel.config(text="")
        else:
            messagebox.showerror("IP Adress Error", "Enter a Valid IP Address")
            return

    connected = False  # boolean varible to check whether client is connected to server or not

    mainWin = ThemedTk(theme="breeze")
    mainWin.title("Human DB")
    mainWin.iconbitmap("Images/iconbitmap.ico")
    mainWin.resizable(False, False)

    brandFrame = ttk.Frame(mainWin)

    logoImg = Image.open("Images/logo.png")  # Opens Logo Image
    logoImg = ImageTk.PhotoImage(logoImg.resize((75, 75), Image.ANTIALIAS))

    # Branding Done in brandFrame
    brandLogo = ttk.Label(brandFrame, image=logoImg)
    brandName = ttk.Label(brandFrame, text="Human DB", font=("Helvetica", 22))

    # Placing Frame and brandFrame Subwidgets
    brandLogo.grid(row=0, column=0, padx=5, pady=5)
    brandName.grid(row=0, column=1, padx=5, pady=5)
    brandFrame.grid(row=0, column=0, padx=5, pady=5)

    ipFrame = ttk.Frame(mainWin)

    if os.path.isfile("./server.IP"):
        fileRead = open("server.IP", "r")
        ip = fileRead.read()
        fileRead.close()

        if ip != "":
            ipConnectButton = ttk.Button(ipFrame, text="Connect to Server at IP : " + ip,
                                         command=ipConnectButtonOnClick)
            ipConnectButton.grid(row=0, column=0, padx=5, pady=5)

    ipLabel = ttk.Label(ipFrame, text="Enter IP Address of Server")
    ipEntry = ttk.Entry(ipFrame, justify="center")
    connectButton = ttk.Button(ipFrame, text="Connect to Server", command=connectButtonOnClick)

    ipLabel.grid(row=1, column=0, padx=5, pady=5)
    ipEntry.grid(row=2, column=0, padx=5, pady=5)
    connectButton.grid(row=3, column=0, padx=5, pady=5)

    ipFrame.grid(row=1, column=0, padx=5, pady=5)

    statusLabel = ttk.Label(mainWin)
    statusLabel.grid(row=2, column=0, padx=5, pady=5)

    ipEntry.bind("<Return>", lambda event: connectButtonOnClick())  # binding ipEntry widget to enter key press

    mainWin.mainloop()

    try:
        mainWin.destroy()
    except Exception:
        pass

    return connected
