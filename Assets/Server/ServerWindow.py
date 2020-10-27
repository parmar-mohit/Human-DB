from socket import gethostname, gethostbyname
from tkinter import ttk, Toplevel, BooleanVar, messagebox, Checkbutton

from pandas import Series
from ttkthemes import ThemedTk

from Assets.Classes.Course import Course
from Assets.Classes.Listbox import Listbox
from Assets.file_func import get_file, save_file
from Assets.write_log import write_log


# ServerWindow class shows a window where user can interact with database
# although the class has many function the only method one might call is show_window
# other methods are called by the instance of class for several task
class ServerWindow:
    def __init__(self, server_socket):
        self.serverSocket = server_socket
        self.exit = False

    def add_course_button_on_click(self):
        def add_course():
            nonlocal coursenameEntry, intakeEntry, yearEntry, checkDict, root

            coursename = coursenameEntry.get()
            if coursename == "":
                messagebox.showwarning("Coursename Error", "Coursename cannot be Empty", parent=root)
                return

            year = yearEntry.get()
            if year == "":
                messagebox.showwarning("Year Error", "Year Cannot be Empty", parent=root)
                return

            try:
                year = int(year)
            except ValueError:
                messagebox.showwarning("Year Error", "Year Should be Integer", parent=root)
                return

            intake = intakeEntry.get()
            if intake == "":
                messagebox.showwarning("Intake Error", "Intake Cannot be Empty", parent=root)
                return

            try:
                intake = int(intake)
            except ValueError:
                messagebox.showwarning("Intake Error", "Intake Should be an Integer", parent=root)
                return

            coursename = Course.coursename_check(coursename)

            courseSeries = Series({"Intake": intake, "Year": year}, name=coursename)
            course = Course(course_series=courseSeries)
            course.add_dataframe()
            course.make_directories()
            permissionSeries = Series({"admin": (True, True)}, name=coursename)
            for username, permission in checkDict.items():
                permissionSeries[username] = (permission[0].get(), permission[1].get())

            course.update_permission(permissionSeries)
            write_log("New Course \"" + coursename + "\" Created")
            self.courseListbox.insert(coursename)
            messagebox.showinfo("Course Created", "New Course " + coursename + " Created", parent=root)
            root.destroy()

        root = Toplevel()
        root.title("Add Course")
        root.iconbitmap("Images/iconbitmap.ico")

        ttk.Label(root, text="Course Name : ").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(root, text="No of Years : ").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(root, text="Intake per Year : ").grid(row=2, column=0, padx=5, pady=5)

        coursenameEntry = ttk.Entry(root)
        yearEntry = ttk.Entry(root)
        intakeEntry = ttk.Entry(root)
        permissionFrame = ttk.Frame(root)
        addcourseButton = ttk.Button(root, text="Add Course", command=add_course)

        coursenameEntry.grid(row=0, column=1, padx=5, pady=5)
        yearEntry.grid(row=1, column=1, padx=5, pady=5)
        intakeEntry.grid(row=2, column=1, padx=5, pady=5)
        permissionFrame.grid(row=0, column=2, rowspan=3, padx=5, pady=5)
        addcourseButton.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # creating and placing child widgets for permissionFrame
        userDataFrame = get_file(".Users")
        checkDict = {}
        if len(userDataFrame.index) > 1:
            ttk.Label(permissionFrame, text="Username").grid(row=0, column=0, rowspan=2, padx=5, pady=5)
            ttk.Label(permissionFrame, text="Permission").grid(row=0, column=1, columnspan=2, padx=5, pady=5)
            ttk.Label(permissionFrame, text="Read").grid(row=1, column=1, padx=5, pady=5)
            ttk.Label(permissionFrame, text="Write").grid(row=1, column=2, padx=5, pady=5)

            row = 2

            for username in userDataFrame.index:
                if username != "admin":
                    ttk.Label(permissionFrame, text=username).grid(row=row, column=0, padx=5, pady=5)
                    readCheckVal = BooleanVar()
                    writeCheckVal = BooleanVar()
                    readCheckVal.set(False)
                    writeCheckVal.set(False)
                    ttk.Checkbutton(permissionFrame, variable=readCheckVal, onvalue=True, offvalue=False).grid(row=row,
                                                                                                               column=1,
                                                                                                               padx=5,
                                                                                                               pady=5)
                    ttk.Checkbutton(permissionFrame, variable=writeCheckVal, onvalue=True, offvalue=False).grid(row=row,
                                                                                                                column=2,
                                                                                                                padx=5,
                                                                                                                pady=5)
                    row += 1
                    checkDict[username] = (readCheckVal, writeCheckVal)

        root.mainloop()

    def client_connection_button_on_click(self):
        if self.serverSocket.acceptConnection:
            self.serverSocket.acceptConnection = False
            write_log("Closing Connection with all Clients")
            self.serverSocket.close_all_connections()
            self.clientConnectionButton["text"] = "Start Accepting Connections"
            self.serverInfoLabel.config(text="Server is Down")
        else:
            write_log("Started Accepting Client Connection")
            self.serverSocket.acceptConnection = True
            self.clientConnectionButton["text"] = "Close Connection with all Clients"
            self.serverInfoLabel.config(text="Server is up and running at IP : {}".format(gethostbyname(gethostname())))

    def connected_client_button_on_click(self):
        def client_select(event):
            nonlocal detailsFrame, connnectedListbox

            addr = connnectedListbox.get()["text"]
            client = self.serverSocket.connected[addr]

            for widget in detailsFrame.winfo_children():
                widget.destroy()

            ttk.Label(detailsFrame, text="IP Address : {}".format(str(addr))).grid(row=0, column=0, padx=5, pady=5)
            if client.user is None:
                ttk.Label(detailsFrame, text="User Details not Found").grid(row=1, column=0, padx=5, pady=5)
            else:
                ttk.Label(detailsFrame, text="Username : {}".format(client.user.username)).grid(row=1, column=0, padx=5,
                                                                                                pady=5)
                ttk.Label(detailsFrame,
                          text="Login Time : {}".format(client.user.loginDateTime.stftime("%d/%m/%y %H:%M:%S"))).grid(
                    row=2, column=0, padx=5, pady=5)

        def close_connection():
            nonlocal connnectedListbox, root

            addr = connnectedListbox.get()["text"]
            if addr == "":
                messagebox.showwarning("Selection Error", "Select Client with whom you want to close Connection",
                                       parent=root)
                return
            client = self.serverSocket.connected[addr]
            client.close_connection(True)
            connnectedListbox.delete_selected()

        if len(self.serverSocket.connected) == 0:
            messagebox.showwarning("No Client Connected", "No Client is Connected to Server")
            return

        root = Toplevel()
        root.title("Connected Users")
        root.iconbitmap("Images/iconbitmap.ico")

        connnectedListbox = Listbox(root, "IP Adresss", 6, 150)
        detailsFrame = ttk.LabelFrame(root, text="Client Details")
        closeClientButton = ttk.Button(root, text="Close Connection with Client", command=close_connection)

        connnectedListbox.grid(row=0, column=0, padx=5, pady=5)
        detailsFrame.grid(row=0, column=1, padx=5, pady=5)
        closeClientButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        for addr in self.serverSocket.connected.keys():
            connnectedListbox.insert(str(addr))

        connnectedListbox.treeview.bind("<<TreeviewSelect>>", client_select)

        root.mainloop()

    def delete_course_button_on_click(self):
        coursename = self.courseListbox.get()["text"]
        if coursename == "":
            messagebox.showwarning("Course Selection", "Select a Course to Delete", parent=self.mainWin)
            return

        response = messagebox.askokcancel("Delete " + coursename,
                                          "Are you sure you want ti delete " + coursename + " Course ?",
                                          parent=self.mainWin)
        if not response:
            return
        self.courseListbox.delete_selected()
        course = Course(coursename=coursename)
        course.delete_course()
        write_log(coursename + " Course Deleted")

    def edit_permission_button_on_click(self):
        def save_changes_button_on_click():
            nonlocal checkDict, coursename, root
            permissionSeries = Series({"admin": (True, True)}, name=coursename)
            for username, permission in checkDict.items():
                permissionSeries[username] = (permission[0].get(), permission[1].get())

            course = Course(coursename=coursename)
            course.update_permission(permissionSeries)
            write_log("Read/Write Permission Changed for " + coursename)
            root.destroy()

        coursename = self.courseListbox.get()["text"]

        if coursename == "":
            messagebox.showwarning("Course Selection Error", "Select a Course to edit Permissions", parent=self.mainWin)
            return

        root = Toplevel()
        root.title("Edit Permission")
        root.iconbitmap("Images/iconbitmap.ico")
        ttk.Label(root, text="Username").grid(row=0, column=0, rowspan=2, padx=5, pady=5)
        ttk.Label(root, text="Permission").grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        ttk.Label(root, text="Read").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(root, text="Write").grid(row=1, column=2, padx=5, pady=5)

        row = 2
        userDataFrame = get_file(".Users")
        checkDict = {}
        for username in userDataFrame.index:
            if username != "admin":
                ttk.Label(root, text=username).grid(row=row, column=0, padx=5, pady=5)
                readCheckVal = BooleanVar()
                writeCheckVal = BooleanVar()
                ttk.Checkbutton(root, variable=readCheckVal, onvalue=True, offvalue=False).grid(row=row, column=1,
                                                                                                padx=5, pady=5)
                ttk.Checkbutton(root, variable=writeCheckVal, onvalue=True, offvalue=False).grid(row=row, column=2,
                                                                                                 padx=5, pady=5)
                permission = userDataFrame.loc[username, coursename]
                if permission[0]:
                    readCheckVal.set(True)
                else:
                    readCheckVal.set(False)
                if permission[1]:
                    writeCheckVal.set(True)
                else:
                    writeCheckVal.set(False)
                row += 1
                checkDict[username] = (readCheckVal, writeCheckVal)

        ttk.Button(root, text="Save Changes", command=save_changes_button_on_click).grid(row=row, column=0,
                                                                                         columnspan=3, padx=5, pady=5)

        root.mainloop()

    def refresh_course_listbox(self):
        courseDataFrame = get_file("Courses/Course.DF")
        self.courseListbox.delete_all()

        for coursename in courseDataFrame.index:
            self.courseListbox.insert(coursename)

    def show_window(self):
        self.mainWin = ThemedTk(theme="breeze")
        self.mainWin.title("Human DB")
        self.mainWin.iconbitmap("Images/iconbitmap.ico")

        # creating and placing child widgets for mainWin
        databaseFrame = ttk.LabelFrame(self.mainWin, text="Database")
        serverOptionsFrame = ttk.LabelFrame(self.mainWin, text="Server Options")
        serverInfoFrame = ttk.LabelFrame(self.mainWin, text="Server Info")

        databaseFrame.grid(row=0, column=0, padx=5, pady=5, sticky="NS")
        serverOptionsFrame.grid(row=0, column=1, padx=5, pady=5)
        serverInfoFrame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="EW")

        # creating and placing child widgets for databaseFrame
        self.courseListbox = Listbox(databaseFrame, "Courses", 5, 200)
        self.refresh_course_listbox()
        addCourseButton = ttk.Button(databaseFrame, text="Add Course", command=self.add_course_button_on_click)
        editPermissionButton = ttk.Button(databaseFrame, text="Edit Permission",
                                          command=self.edit_permission_button_on_click)
        deleteCourse = ttk.Button(databaseFrame, text="Delete Course", command=self.delete_course_button_on_click)

        self.courseListbox.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
        addCourseButton.grid(row=0, column=1, padx=5, pady=5)
        editPermissionButton.grid(row=1, column=1, padx=5, pady=5)
        deleteCourse.grid(row=2, column=1, padx=5, pady=5)

        # creating and placing child widgets in serverOptionsFrame
        connectedClientButton = ttk.Button(serverOptionsFrame, text="View Connected Clients",
                                           command=self.connected_client_button_on_click)
        usersButton = ttk.Button(serverOptionsFrame, text="View Users Details", command=self.users_button_on_click)
        self.clientConnectionButton = ttk.Button(serverOptionsFrame, command=self.client_connection_button_on_click)
        if self.serverSocket.acceptConnection:
            self.clientConnectionButton["text"] = "Close Connection with all Clients"
        else:
            self.clientConnectionButton["text"] = "Start Accepting Connections"
        logoutButton = ttk.Button(serverOptionsFrame, text="Log Out", command=self.mainWin.destroy)
        stopServerButton = ttk.Button(serverOptionsFrame, text="Stop Server And Quit Program",
                                      command=self.stop_server_button_on_click)

        connectedClientButton.grid(row=0, column=0, padx=5, pady=5)
        usersButton.grid(row=1, column=0, padx=5, pady=5)
        self.clientConnectionButton.grid(row=2, column=0, padx=5, pady=5)
        logoutButton.grid(row=3, column=0, padx=5, pady=5)
        stopServerButton.grid(row=4, column=0, padx=5, pady=5)

        # creating and placing child for serverInfoFrame
        self.serverInfoLabel = ttk.Label(serverInfoFrame, justify="center")
        if self.serverSocket.acceptConnection:
            self.serverInfoLabel["text"] = "Server is up and running at IP : " + gethostbyname(gethostname())
        else:
            self.serverInfoLabel["text"] = "Server is Down"

        self.serverInfoLabel.pack(padx=5, pady=5)

        self.mainWin.mainloop()

        return self.exit

    def stop_server_button_on_click(self):
        self.exit = True
        self.mainWin.destroy()

    def users_button_on_click(self):
        def user_select(event):
            nonlocal userDetailsFrame, userDataFrame, userListbox

            try:
                for widget in userDetailsFrame.winfo_children():
                    widget.destroy()
            except:
                pass

            username = userListbox.get()["text"]
            userSeries = userDataFrame.loc[username]

            ttk.Label(userDetailsFrame,
                      text="Name : {} {}".format(userSeries["First Name"], userSeries["Last Name"])).grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=5,
                                                                                                          pady=5)
            ttk.Label(userDetailsFrame, text="Username : {}".format(username)).grid(row=1, column=0, padx=5, pady=5)
            if userSeries["Last Login Date"] is None:
                ttk.Label(userDetailsFrame, text="Last Login Date : No Details Found").grid(row=2,
                                                                                            column=0,
                                                                                            padx=5,
                                                                                            pady=5)
            else:
                ttk.Label(userDetailsFrame, text="Last Login Date : {}".format(
                    userSeries["Last Login Date"].strftime("%d/%m/%y %H:%M:%S"))).grid(row=2,
                                                                                       column=0,
                                                                                       padx=5,
                                                                                       pady=5)
            if userSeries["Last Logout Date"] is None:
                ttk.Label(userDetailsFrame, text="Last Logout Date : No Details Found").grid(row=3,
                                                                                             column=0,
                                                                                             padx=5,
                                                                                             pady=5)
            else:
                ttk.Label(userDetailsFrame, text="Last Logout Date : {}".format(
                    userSeries["Last Logout Date"].strftime("%d/%m/%y %H:%M:%S"))).grid(row=3,
                                                                                        column=0,
                                                                                        padx=5,
                                                                                        pady=5)

            userFrame = ttk.Frame(userDetailsFrame)
            userFrame.grid(row=0, column=1, rowspan=4, padx=5, pady=5)

            # creating and placing child widget for userFrame
            ttk.Label(userFrame, text="Course").grid(row=0, column=0, rowspan=2, padx=5, pady=5)
            ttk.Label(userFrame, text="Permission").grid(row=0, column=1, columnspan=2, padx=5, pady=5)
            ttk.Label(userFrame, text="Read").grid(row=1, column=1, padx=5, pady=5)
            ttk.Label(userFrame, text="Write").grid(row=1, column=2, padx=5, pady=5)

            row = 2
            courseList = get_file("Courses/Course.DF").index
            for coursename in courseList:
                ttk.Label(userFrame, text=coursename).grid(row=row, column=0, padx=5, pady=5)
                readCheckbutton = Checkbutton(userFrame, state="disabled")
                writeCheckbutton = Checkbutton(userFrame, state="disabled")
                readCheckbutton.grid(row=row, column=1, padx=5, pady=5)
                writeCheckbutton.grid(row=row, column=2, padx=5, pady=5)
                permission = userDataFrame.loc[username, coursename]
                if permission[0]:
                    readCheckbutton.select()
                else:
                    readCheckbutton.deselect()
                if permission[1]:
                    writeCheckbutton.select()
                else:
                    writeCheckbutton.deselect()
                readCheckbutton.config(state="disabled")
                writeCheckbutton.config(state="disabled")

                row += 1

        def delete_user_button_on_click():
            nonlocal userDataFrame, userListbox, root
            username = userListbox.get()["text"]
            if username == "":
                messagebox.showwarning("User Selection", "Select a user to delete", parent=root)
                return
            if username == "admin":
                messagebox.showwarning("User Selection", "admin User cannot be Deleted", parent=root)
                return

            response = messagebox.askokcancel("Delete User", "Are you Sure you want to delete " + username + " User ?",
                                              parent=root)
            if not response:
                return

            userDataFrame.drop(username, inplace=True)
            save_file(".Users", userDataFrame)

        userDataFrame = get_file(".Users")

        root = Toplevel()
        root.title("Users Details")
        root.iconbitmap("Images/iconbitmap.ico")
        userListbox = Listbox(root, "Users", 5, 125)

        userDetailsFrame = ttk.LabelFrame(root, text="Users Details")
        ttk.Button(root, text="Delete User", command=delete_user_button_on_click).grid(row=1, column=0, columnspan=2,
                                                                                       padx=5, pady=5)

        userListbox.grid(row=0, column=0, padx=5, pady=5)
        userDetailsFrame.grid(row=0, column=1, padx=5, pady=5)

        for username in userDataFrame.index:
            userListbox.insert(username)

        userListbox.treeview.bind("<<TreeviewSelect>>", user_select)
        root.mainloop()
