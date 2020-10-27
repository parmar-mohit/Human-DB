from tkinter import ttk, Toplevel, messagebox

from PIL import ImageTk, Image
from pandas import Series
from ttkthemes import ThemedTk

from Assets.Classes.User import User


# client_login function provides gui to login or to create a new user
# it return 3 variables one is a valid variable which is set to true if user has successfully logged in
# other is an integer which is new request no and the last one is user object
# if user has successfully logged in else none
def client_login(client_socket, request):
    def login():
        nonlocal usernameEntry, passwordEntry, userDataFrame, valid, user, loginInfoLabel, mainWin

        username = usernameEntry.get()
        usernameEntry.delete(0, "end")
        usernameEntry.insert(0, "username")

        password = passwordEntry.get()
        passwordEntry.delete(0, "end")
        passwordEntry.insert(0, "password")

        if username in userDataFrame.index:
            if User.password_hash(password) == userDataFrame.loc[username, "Password"]:
                valid = True
                user = User(user_series=userDataFrame.loc[username])
                user.password = userDataFrame.loc[username, "Password"]
                loginInfoLabel.config(text="Login Succesfull")
                mainWin.destroy()
            else:
                loginInfoLabel.config(text="Invalid Credentials")
        else:
            loginInfoLabel.config(text="Invalid Credentials")

    def create_user():
        def create_user_button_on_click():
            nonlocal firstnameEntry, lastnameEntry, root, userDataFrame
            nonlocal usernameEntry, passwordEntry, confirmPasswordEntry
            nonlocal client_socket, request

            firstname = firstnameEntry.get()
            if firstname == "":
                messagebox.showwarning("First Name Error", "First Name Cannot be Empty", parent=root)
                return

            lastname = lastnameEntry.get()
            if lastname == "":
                messagebox.showwarning("Last Name Error", "Last Name Cannot be Empty", parent=root)
                return

            username = usernameEntry.get()
            if username == "":
                messagebox.showwarning("Username Error", "Username cannot be empty", parent=root)
                return

            if User.username_check(username):
                messagebox.showwarning("Username Error",
                                       "Username cannot contain spaces or have special characters other than underscore",
                                       parent=root)
                return

            if username in userDataFrame.index:
                messagebox.showwarning("Username Error", "Username is taken,Choose other Username", parent=root)
                return

            password = passwordEntry.get()
            if password == "":
                messagebox.showwarning("Password Error", "Password cannot be empty", parent=root)
                return

            if not User.password_check(password):
                messagebox.showwarning("Password Error",
                                       "Password must have an uppercase letter, lowercase letter and a number",
                                       parent=root)
                return

            confirmPassword = confirmPasswordEntry.get()
            if confirmPassword != password:
                messagebox.showwarning("Password Error", "Passwords do not match", parent=root)
                return

            userSeries = Series({"First Name": firstname,
                                 "Last Name": lastname,
                                 "Password": password,
                                 "Last Login Date": None,
                                 "Last Logout Date": None}, name=username)

            try:
                for coursename in userDataFrame.columns[5:]:
                    userSeries[coursename] = (False, False)
            except:
                pass

            user = User(user_series=userSeries)
            userDataFrame = userDataFrame.append(userSeries)
            userDataFrame.loc[username, "Password"] = user.password
            client_socket.add_new_user(user, request)
            request += 1

            messagebox.showinfo("User Created", "New User with username " + username + " created", parent=root)
            root.destroy()

        root = Toplevel()
        root.title("Create User")
        root.iconbitmap("Images/iconbitmap.ico")

        firstnameEntry = ttk.Entry(root, justify="center")
        lastnameEntry = ttk.Entry(root, justify="center")
        usernameEntry = ttk.Entry(root, justify="center")
        passwordEntry = ttk.Entry(root, show="*", justify="center")
        confirmPasswordEntry = ttk.Entry(root, show="*", justify="center")

        ttk.Label(root, text="First Name").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(root, text="Last Name").grid(row=0, column=1, padx=5, pady=5)
        firstnameEntry.grid(row=1, column=0, padx=5, pady=5)
        lastnameEntry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Username").grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        usernameEntry.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        ttk.Label(root, text="Password").grid(row=4, column=0, padx=5, pady=5)
        ttk.Label(root, text="Confirm Password").grid(row=4, column=1, padx=5, pady=5)
        passwordEntry.grid(row=5, column=0, padx=5, pady=5)
        confirmPasswordEntry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(root, text="Create User", command=create_user_button_on_click).grid(row=6, column=0, columnspan=2,
                                                                                       padx=5, pady=5)

        root.mainloop()

    valid = False
    user = None
    userDataFrame = client_socket.request_user_dataframe(request)
    request += 1

    mainWin = ThemedTk(theme="breeze")
    mainWin.title("Human DB")
    mainWin.iconbitmap("Images/iconbitmap.ico")

    brandFrame = ttk.Frame(mainWin)
    loginFrame = ttk.Frame(mainWin)

    brandFrame.grid(row=0, column=0, padx=5, pady=5)
    loginFrame.grid(row=1, column=0, padx=5, pady=5)

    logoImg = Image.open("Images/logo.png")  # Opens Logo Image
    logoImg = ImageTk.PhotoImage(logoImg.resize((75, 75), Image.ANTIALIAS))

    # Branding Done in brandFrame
    brandLogo = ttk.Label(brandFrame, image=logoImg)
    brandName = ttk.Label(brandFrame, text="Human DB", font=("Helvetica", 22))

    # Placing Frame and brandFrame Subwidgets
    brandLogo.grid(row=0, column=0, padx=5, pady=5)
    brandName.grid(row=0, column=1, padx=5, pady=5)

    # creating and placing child widgets for loginFrame

    usernameEntry = ttk.Entry(loginFrame, justify="center")
    passwordEntry = ttk.Entry(loginFrame, justify="center", show="*")
    ttk.Button(loginFrame, text="Login", command=login).grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(loginFrame, text="Create User", command=create_user).grid(row=3, column=0, padx=5, pady=5)
    loginInfoLabel = ttk.Label(loginFrame)

    usernameEntry.insert(0, "username")
    passwordEntry.insert(0, "password")

    usernameEntry.bind("<Button-1>", lambda event: usernameEntry.delete(0, "end"))
    passwordEntry.bind("<Button-1>", lambda event: passwordEntry.delete(0, "end"))
    usernameEntry.bind("<Return>", lambda event: login())
    passwordEntry.bind("<Return>", lambda event: login())

    usernameEntry.grid(row=0, column=0, padx=5, pady=5)
    passwordEntry.grid(row=1, column=0, padx=5, pady=5)
    loginInfoLabel.grid(row=4, column=0, padx=5, pady=5)

    mainWin.mainloop()

    return valid, request, user
