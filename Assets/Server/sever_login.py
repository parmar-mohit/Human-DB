from socket import gethostname, gethostbyname
from tkinter import ttk

from ttkthemes import ThemedTk

from Assets.Classes.ServerSocket import ServerSocket
from Assets.Classes.User import User


# server_login function creates a window and ask user to enter username and password
# only admin user can access this account if other user try to login to program
# they get message saying "Invalid Credentials" and the function return a boolean value
# function return True if user has succesfully logged in else it returns False
def server_login(server_socket: ServerSocket):
    def login_button_on_click():
        nonlocal loginLabel, usernameEntry, passwordEntry, mainWin, userLogin, serverInfoLabel
        username = usernameEntry.get()
        password = passwordEntry.get()

        usernameEntry.delete(0, "end")
        passwordEntry.delete(0, "end")

        usernameEntry.insert(0, "username")
        passwordEntry.insert(0, "password")

        user = User(username="admin")

        if username == "admin" and User.password_hash(password) == user.password:
            userLogin = True
            serverInfoLabel.destroy()
            mainWin.destroy()
        else:
            loginLabel.config(text="Invalid Credentials")

    userLogin = False

    mainWin = ThemedTk(theme="breeze")
    mainWin.title("Human DB")
    mainWin.iconbitmap("Images/iconbitmap.ico")
    mainWin.resizable(False, False)

    # creating and placing child widget for mainWin
    serverInfoFrame = ttk.LabelFrame(mainWin, text="Server Info")
    loginFrame = ttk.Frame(mainWin)

    serverInfoFrame.grid(row=0, column=0, padx=5, pady=5, rowspan=5, sticky="NS")
    loginFrame.grid(row=0, column=1, padx=5, pady=5)

    # creating and placing child Widgets for serverInfo Frame
    serverInfoLabel = ttk.Label(serverInfoFrame, justify="center")
    if server_socket.acceptConnection:
        serverInfoLabel["text"] = "Server is up and running at IP : " + gethostbyname(gethostname())
    else:
        serverInfoLabel["text"] = "Server is Down"
    serverInfoLabel.pack(padx=5, ipady=60)

    # creating and placing child widgets for loginFrame
    ttk.Label(loginFrame, text="Human DB", font=("Helvetica", 22)).grid(row=0, column=0, padx=5, pady=5)

    usernameEntry = ttk.Entry(loginFrame, justify="center")
    passwordEntry = ttk.Entry(loginFrame, justify="center", show="*")

    usernameEntry.insert(0, "username")
    passwordEntry.insert(0, "password")

    usernameEntry.bind("<Button-1>", lambda event: usernameEntry.delete(0, "end"))
    passwordEntry.bind("<Button-1>", lambda event: passwordEntry.delete(0, "end"))
    usernameEntry.bind("<Return>", lambda event: login_button_on_click())
    passwordEntry.bind("<Return>", lambda event: login_button_on_click())

    usernameEntry.grid(row=1, column=0, padx=5, pady=5)
    passwordEntry.grid(row=2, column=0, padx=5, pady=5)

    ttk.Button(loginFrame, text="Login", command=login_button_on_click).grid(row=3, column=0, padx=5, pady=5)

    loginLabel = ttk.Label(loginFrame)
    loginLabel.grid(row=4, column=0, padx=5, pady=5)

    mainWin.mainloop()

    return userLogin
