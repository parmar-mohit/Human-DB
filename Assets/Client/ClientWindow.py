from time import sleep
from tkinter import ttk, Toplevel, messagebox, StringVar

from pandas import Series
from ttkthemes import ThemedTk

from Assets.Classes.DateEntry import DateEntry
from Assets.Classes.ScrollFrame import ScrollFrame
from Assets.Classes.Student import Student
from Assets.Classes.StudentFrame import StudentFrame


class ClientWindow:
    def __init__(self, client_socket, user, request):
        self.clientSocket = client_socket
        self.user = user
        self.request = request
        self.quit = True

    def add_attendance(self):
        def add_attendance_button_on_click():
            nonlocal dateEntry, attendanceDict, root
            nonlocal coursename, year

            attendanceDate = dateEntry.get()
            if attendanceDate is None:
                messagebox.showerror("Date not Selected", "Please Enter a Date", parent=root)
                return

            attendanceSeries = Series(name=attendanceDate)
            for sid, var in attendanceDict.items():
                if var.get() == "Present":
                    attendanceSeries[sid] = True
                elif var.get() == "Absent":
                    attendanceSeries[sid] = False
                else:
                    messagebox.showwarning("Attendance Error", "Select attendnace for student with SID " + sid,
                                           parent=root)
                    return

            self.clientSocket.add_attendance(coursename, year, attendanceSeries, self.request)
            self.request += 1

            messagebox.showinfo("Attendance Added", "Attendance for date {} was added".format(attendanceDate),
                                parent=root)
            root.destroy()

        def present_button_on_click():
            nonlocal attendanceDict

            for var in attendanceDict.values():
                if var.get() == "N/A":
                    var.set("Present")

        def absent_button_on_click():
            nonlocal attendanceDict

            for var in attendanceDict.values():
                if var.get() == "N/A":
                    var.set("Absent")

        def clear_button_on_click():
            nonlocal attendanceDict

            for var in attendanceDict.values():
                var.set("N/A")

        selectedObj = self.courseTreeview.item(self.courseTreeview.focus())

        try:
            year = selectedObj["values"][1]
        except IndexError:
            messagebox.showwarning("Select Course", "You Must Select a Course")
            return

        if year == 0:
            self.statusLabel.config(text="Status : Select the Course Year")
            return

        coursename = selectedObj["values"][0]

        if not self.user.dbPermission[coursename][1]:
            self.statusLabel.config(text="Status : You don't have write Permission for " + coursename)
            return

        self.statusLabel.config(text="Status : Getting data From Server")

        studentDataFrame = self.clientSocket.student_dataframe(coursename, year, self.request)
        self.request += 1

        root = Toplevel()
        root.title("Add Attendance")
        root.iconbitmap("Images/iconbitmap.ico")

        screenSize = (root.winfo_screenwidth() - 60, 500)

        ttk.Label(root, text="Attendace for Date : ").grid(row=0, column=0, padx=5, pady=5)
        dateEntry = DateEntry(root)
        attendanceFrame = ScrollFrame(root, text="Add Attedance", width=screenSize[0], height=screenSize[1],
                                      horizontal=True)
        buttonFrame = ttk.Frame(root)
        ttk.Button(root, text="Add Attendance", command=add_attendance_button_on_click).grid(row=2, column=1, padx=5,
                                                                                             pady=5)

        dateEntry.grid(row=0, column=1, padx=5, pady=5)
        attendanceFrame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        buttonFrame.grid(row=2, column=0, padx=5, pady=5)

        # creating and placing child widget for attendanceFrame
        studentDataFrame.sort_values("Roll No")

        attendanceDict = {}
        # attendance dict contains a dictionary with sid as key and a tuple
        # containing presentRadiobutton,absentRadioButton and varible for the radioButton
        rowNo = 0
        columnNo = 0

        for index, row in studentDataFrame.iterrows():
            newFrame = ttk.Frame(attendanceFrame.frame, relief="groove")
            newFrame.grid(row=rowNo, column=columnNo, padx=5, pady=5)

            attendanceStringVar = StringVar()
            attendanceStringVar.set("N/A")

            ttk.Label(newFrame, text=row["First Name"]).grid(row=0, column=0, padx=5, pady=5)
            ttk.Label(newFrame, text=row["Last Name"]).grid(row=0, column=1, padx=5, pady=5)
            ttk.Radiobutton(newFrame, text="Present", variable=attendanceStringVar,
                            value="Present").grid(row=0, column=2, padx=5, pady=5)
            ttk.Label(newFrame, text="SID : " + index).grid(row=1, column=0, padx=5, pady=5)
            ttk.Label(newFrame, text="Roll No : " + row["Roll No"]).grid(row=1, column=1, padx=5, pady=5)
            ttk.Radiobutton(newFrame, text="Absent", variable=attendanceStringVar,
                                                value="Absent").grid(row=1, column=2, padx=5, pady=5)

            attendanceDict[index] = attendanceStringVar

            if columnNo == 4:
                columnNo = 0
                rowNo += 1
            else:
                columnNo += 1

        # creating and placing child widgets for buttonFrame
        ttk.Button(buttonFrame, text="Mark Unmarked as Present", command=present_button_on_click).grid(row=0, column=0,
                                                                                                       padx=5, pady=5)
        ttk.Button(buttonFrame, text="Mark Unmarked as Absent", command=absent_button_on_click).grid(row=0, column=1,
                                                                                                     padx=5, pady=5)
        ttk.Button(buttonFrame, text="Clear", command=clear_button_on_click).grid(row=0, column=2, padx=5, pady=5)

        root.mainloop()

    def add_student(self):
        def add_student_button_on_click():
            nonlocal studentFrame, root
            studentSeries = Series()
            firstname = studentFrame.firstnameEntry.get()

            if firstname == "":
                messagebox.showwarning("Name Error", "First Name cannot be empty", parent=root)
                return
            studentSeries["First Name"] = firstname

            lastname = studentFrame.lastnameEntry.get()
            if lastname == "":
                messagebox.showwarning("Name Error", "Last Name cannot be empty", parent=root)
                return
            studentSeries["Last Name"] = lastname

            fathername = studentFrame.fathernameEntry.get()
            if fathername == "":
                fathername = None
            studentSeries["Father Name"] = fathername

            mothername = studentFrame.mothernameEntry.get()
            if mothername == "":
                mothername = None
            studentSeries["Mother Name"] = mothername

            dob = studentFrame.dobEntry.get()
            if dob is None:
                messagebox.showwarning("DOB Error", "Enter date of birth", parent=root)
                return
            studentSeries["DOB"] = dob

            gender = studentFrame.genderStringVar.get()
            if gender == "N/A":
                messagebox.showwarning("Gender Error", "Select Gender", parent=root)
                return
            studentSeries["Gender"] = gender

            phoneNo = studentFrame.phoneEntry.get()
            try:
                int(phoneNo)
            except:
                messagebox.showwarning("Phone No Error", "Enter a correct Phone Number", parent=root)
                return
            studentSeries["Phone No"] = phoneNo

            email = studentFrame.emailEntry.get()
            if email == "":
                email = None
            studentSeries["Email"] = email

            parentPhoneNo = studentFrame.parentPhoneEntry.get()
            try:
                int(parentPhoneNo)
            except:
                messagebox.showwarning("Phone No Error", "Enter a correct parent Phone No", parent=root)
                return
            studentSeries["Parent Phone No"] = parentPhoneNo

            parentEmail = studentFrame.parentEmailEntry.get()
            if parentEmail == "":
                parentEmail = None
            studentSeries["Parent Email"] = parentEmail

            address = studentFrame.addressEntry.get()
            if address == "":
                messagebox.showwarning("Address Error", "Address cannot be empty", parent=root)
                return

            city = studentFrame.cityEntry.get()
            if city == "":
                messagebox.showwarning("Address Error", "City cannot be empty", parent=root)
                return

            state = studentFrame.stateEntry.get()
            if state == "":
                messagebox.showwarning("Address Error", "State name cannot be Empty", parent=root)
                return

            pincode = studentFrame.pincodeEntry.get()
            try:
                int(pincode)
            except:
                messagebox.showwarning("Address Error", "Enter a correct pincode", parent=root)
                return
            studentSeries["Address"] = {"address": address, "city": city, "state": state, "pincode": pincode}

            course = studentFrame.courseStringVar.get()
            if course == "":
                messagebox.showwarning("Course Error", "Select a Course", parent=root)
                return
            studentSeries["Course Name"] = course

            year = studentFrame.yearIntVar.get()
            if year == 0:
                messagebox.showwarning("Year Error", "Select a Year", parent=root)
                return
            studentSeries["Year"] = year

            sid = studentFrame.sidEntry.get()
            if sid == "":
                messagebox.showwarning("SID Error", "Enter SID of Student", parent=root)
                return
            studentSeries.name = sid

            rollNo = studentFrame.rollEntry.get()
            if rollNo == "":
                messagebox.showwarning("Roll No Error", "Enter Roll No of Student", parent=root)
                return
            studentSeries["Roll No"] = rollNo

            personImage = studentFrame.image
            studentSeries["Image"] = personImage
            signImage = studentFrame.signImage
            studentSeries["Sign Image"] = signImage

            student = Student(student_series=studentSeries)

            status = self.clientSocket.add_student(student, self.request)
            self.request += 1

            if status == 1:
                messagebox.showwarning("Student not added to Databse",
                                       "Student was not added to databace cause another student has same sid as entered for this student",
                                       parent=root)
                return
            elif status == 2:
                messagebox.showwarning("Student not added to database",
                                       "Student was not added to database cause intake for Year {} course {} was full".format(
                                           year, course), parent=root)
                return
            elif status == 3:
                messagebox.showinfo("Student added to database", "Student was added to database sucesfully",
                                    parent=root)
                root.destroy()

        writePermission = {coursename: self.courseDataFrame.loc[coursename, "Year"] for coursename in
                           self.user.dbPermission.keys() if self.user.dbPermission[coursename][1]}

        root = Toplevel()
        root.title("Add Student")
        root.iconbitmap("Images/iconbitmap.ico")

        studentFrame = StudentFrame(root, write_permission=writePermission)
        studentFrame.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(root, text="Add Student", command=add_student_button_on_click).grid(row=1, column=0, padx=5, pady=5)

        root.mainloop()

    def change_password(self):
        def change_password_button_on_click():
            nonlocal oldPasswordEntry, passwordEntry, confirmPasswordEntry, root
            oldPassword = oldPasswordEntry.get()

            if self.user.password_hash(oldPassword) != self.user.password:
                messagebox.showwarning("Password Error", "Old Password do not match", parent=root)
                return

            password = passwordEntry.get()

            if password == "":
                messagebox.showwarning("Password Error", "Password cannot be empty", parent=root)
                return

            if not self.user.password_check(password):
                messagebox.showwarning("Password Error",
                                       "Password must have an uppercase letter, lowercase letter and a number",
                                       parent=root)
                return

            confirmPassword = confirmPasswordEntry.get()
            if confirmPassword != password:
                messagebox.showwarning("Password Error", "Passwords do not match", parent=root)
                return

            self.clientSocket.change_password(self.user.username, self.user.password_hash(password), self.request)
            self.request += 1

            messagebox.showinfo("Password Changes", "Your Password has been Changed", parent=root)
            root.destroy()

        if self.user.username == "admin":
            messagebox.showwarning("Username Error", "Username cannot be changed for admin User")
            return

        root = Toplevel()
        root.title("Change Password")
        root.iconbitmap("Images/iconbitmap.ico")

        oldPasswordEntry = ttk.Entry(root, show="*", justify="center")
        passwordEntry = ttk.Entry(root, show="*", justify="center")
        confirmPasswordEntry = ttk.Entry(root, show="*", justify="center")

        ttk.Label(root, text="Old Password").grid(row=0, column=0, padx=5, pady=5)
        oldPasswordEntry.grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(root, text="New Password").grid(row=2, column=0, padx=5, pady=5)
        passwordEntry.grid(row=3, column=0, padx=5, pady=5)
        ttk.Label(root, text="Confirm New Password").grid(row=4, column=0, padx=5, pady=5)
        confirmPasswordEntry.grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(root, text="Change Password", command=change_password_button_on_click).grid(row=6, column=0, padx=5,
                                                                                               pady=5)

        root.mainloop()

    def delete_student(self, root):
        selectedObj = self.studentTreeview.item(self.studentTreeview.focus())

        sid = selectedObj["text"]

        if sid == "":
            messagebox.showwarning("Select Student", "Select a Student to Delete Details", parent=root)
            return

        response = messagebox.askokcancel("Delete Student", "Are you sure you want to delete student with sid " + sid,
                                          parent=root)

        if not response:
            return

        self.studentTreeview.delete(self.studentTreeview.focus())
        self.clientSocket.delete_student(sid, self.course[0], self.course[1], self.request)

    def logout_button_on_click(self):
        self.quit = False
        self.mainWin.destroy()

    def refresh_course_treeview(self):
        sleep(7)
        self.courseDataFrame = self.clientSocket.request_course_dataframe(self.request)
        self.request += 1

        # removing data from treeview
        for node in self.courseTreeview.get_children():
            self.courseTreeview.delete(node)

        self.courseDataFrame.sort_index(inplace=True)

        # inserting data in treeview
        no = 1
        for coursename in self.courseDataFrame.index:
            self.courseTreeview.insert(parent="", index="end", iid=no, text=coursename, values=(coursename, 0))
            for i in range(1, int(self.courseDataFrame.loc[coursename, "Year"]) + 1):
                self.courseTreeview.insert(parent=no, index="end", text=coursename + "_" + str(i),
                                           values=(coursename, i))
            no += 1

    def show_window(self):
        self.mainWin = ThemedTk(theme="breeze")
        self.mainWin.title("Human DB")
        self.mainWin.iconbitmap("Images/iconbitmap.ico")

        # creating and placing child widgets for self.mainWin
        editOptionsFrame = ttk.LabelFrame(self.mainWin, text="Edit Options")
        userFrame = ttk.LabelFrame(self.mainWin, text="User Details")
        logoutFrame = ttk.Frame(self.mainWin)

        editOptionsFrame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        userFrame.grid(row=1, column=0, padx=5, pady=5)
        logoutFrame.grid(row=1, column=1, padx=5, pady=5)

        # creating and placing child widgets for editOptionsFrame
        self.statusLabel = ttk.Label(editOptionsFrame, text="Status : Select a Course")
        self.courseTreeview = ttk.Treeview(editOptionsFrame, columns=("Course", "Year"), selectmode="browse", height=5)
        self.courseTreeview.column("#0", width=250)
        self.courseTreeview.column("Course", width=0, stretch="no")
        self.courseTreeview.column("Year", width=0, stretch="no")

        self.courseTreeview.heading("#0", text="Courses")

        self.refresh_course_treeview()

        courseTreeviewScrollbar = ttk.Scrollbar(editOptionsFrame, orient="vertical", command=self.courseTreeview.yview)
        self.courseTreeview.config(yscrollcommand=courseTreeviewScrollbar.set)

        self.statusLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.courseTreeview.grid(row=1, column=0, rowspan=4, padx=5, pady=5)
        courseTreeviewScrollbar.grid(row=1, column=1, rowspan=4, padx=5, pady=5, sticky="NS")
        ttk.Button(editOptionsFrame, text="Show Student List", command=self.show_student_button_on_click).grid(row=1,
                                                                                                               column=2,
                                                                                                               padx=5,
                                                                                                               pady=5)
        ttk.Button(editOptionsFrame, text="Show Attendance List", command=self.show_attendance).grid(row=2, column=2,
                                                                                                     padx=5, pady=5)
        ttk.Button(editOptionsFrame, text="Add Student", command=self.add_student).grid(row=3, column=2, padx=5, pady=5)
        ttk.Button(editOptionsFrame, text="Add Attendance", command=self.add_attendance).grid(row=4, column=2, padx=5,
                                                                                              pady=5)

        # creating and placing child widget for userFrame
        ttk.Label(userFrame, text="Name : {} {}".format(self.user.firstname, self.user.lastname)).grid(row=0, column=0,
                                                                                                       padx=5, pady=5)
        ttk.Label(userFrame, text="Username : " + self.user.username).grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(userFrame, text="Login Time : {}".format(self.user.loginDateTime.strftime("%d/%m/%y %H:%M:%S"))).grid(
            row=2, column=0, padx=5, pady=5)
        ttk.Button(userFrame, text="Change Password", command=self.change_password).grid(row=3, column=0, padx=5,
                                                                                         pady=5)

        # creating and placing child widgets for logoutFrame
        ttk.Button(logoutFrame, text="Log Out", command=self.logout_button_on_click).grid(row=0, column=0, padx=5,
                                                                                          pady=5)
        ttk.Button(logoutFrame, text="Close Program", command=self.mainWin.destroy).grid(row=1, column=0, padx=5,
                                                                                         pady=5)

        self.mainWin.mainloop()

        return self.request, self.quit

    def show_attendance(self):
        selectedObj = self.courseTreeview.item(self.courseTreeview.focus())

        try:
            year = selectedObj["values"][1]
        except IndexError:
            messagebox.showwarning("Select Course", "You Must Select a Course")
            return

        if year == 0:
            self.statusLabel.config(text="Status : Select the Course Year")
            return

        coursename = selectedObj["values"][0]

        if not self.user.dbPermission[coursename][0]:
            self.statusLabel.config(text="Status : You don't have read Permission for " + coursename)
            return

        root = Toplevel()
        root.title(coursename + "_" + str(year))
        root.iconbitmap("Images/iconbitmap.ico")
        screenSize = (root.winfo_screenwidth() - 60, 500)

        attendanceFrame = ScrollFrame(root, text="Attendance Details", width=screenSize[0], height=screenSize[1],
                                      horizontal=True)
        attendanceFrame.pack()

        attendanceDataFrame = self.clientSocket.request_attendance_dataframe(coursename, year, self.request)
        self.request += 1
        column = 1

        for sid in attendanceDataFrame.columns:
            ttk.Label(attendanceFrame.frame, text=sid).grid(row=0, column=column, padx=5, pady=5)
            column += 1

        row = 1
        for date, attendance in attendanceDataFrame.iterrows():
            ttk.Label(attendanceFrame.frame, text="".format(date)).grid(row=row, column=0, padx=5, pady=5)

            column = 0
            for i in tuple(attendance):
                if i:
                    ttk.Label(attendanceFrame.frame, text="Present").grid(row=row, column=column, padx=5, pady=5)
                else:
                    ttk.Label(attendanceFrame.frame, text="Absent").grid(row=row, column=column, padx=5, pady=5)
                column += 1

            row += 1

        root.mainloop()

    def show_student_button_on_click(self):
        selectedObj = self.courseTreeview.item(self.courseTreeview.focus())

        try:
            course = selectedObj["values"][0]
            year = selectedObj["values"][1]
            self.course = (course, year)
        except:
            messagebox.showwarning("Course Error", "Select Course and Year")
            return

        if year == 0:
            self.statusLabel.config(text="Status : Select Course Year")
            return

        if not self.user.dbPermission[course][0]:
            self.statusLabel.config(text="Status : You don't have read permission for this course")
            return

        root = Toplevel()
        root.title(course + "_" + str(year))
        root.iconbitmap("Images/iconbitmap.ico")

        self.studentTreeview = ttk.Treeview(root, columns=("Roll No", "First Name", "Last Name"), selectmode="browse",
                                            height=12)
        studentTreeviewScrollbar = ttk.Scrollbar(root, orient="vertical", command=self.studentTreeview.yview)
        self.studentTreeview.config(yscrollcommand=studentTreeviewScrollbar.set)

        self.studentTreeview.column("#0", width=140, anchor="center")
        self.studentTreeview.column("Roll No", width=95, anchor="center")
        self.studentTreeview.column("First Name", width=180, anchor="center")
        self.studentTreeview.column("Last Name", width=180, anchor="center")

        self.studentTreeview.heading("#0", text="SID")
        self.studentTreeview.heading("Roll No", text="Roll No")
        self.studentTreeview.heading("First Name", text="First Name")
        self.studentTreeview.heading("Last Name", text="Last Name")

        self.studentTreeview.grid(row=0, column=0, padx=5, pady=5)
        studentTreeviewScrollbar.grid(row=0, column=1, sticky="NS", padx=5, pady=5)
        buttonFrame = ttk.Frame(root)
        buttonFrame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(buttonFrame, text="View Student Details", command=lambda: self.view_student_details(root)).grid(
            row=0, column=0, padx=5, pady=5)
        ttk.Button(buttonFrame, text="Delete Student from Database", command=lambda: self.delete_student(root)).grid(
            row=0, column=1, padx=5, pady=5)

        # inserting data into treeview
        self.studentDataFrame = self.clientSocket.student_dataframe(course, year, self.request)
        self.request += 1

        for index, row in self.studentDataFrame.iterrows():
            self.studentTreeview.insert(parent="", index="end", text=index,
                                        values=(row["Roll No"], row["First Name"], row["Last Name"]))

        root.mainloop()

        del self.studentDataFrame, self.studentTreeview, self.course

    def view_student_details(self, root):
        selectedObj = self.studentTreeview.item(self.studentTreeview.focus())

        try:
            sid = selectedObj["text"]
        except:
            messagebox.showwarning("Select Student", "Select a Student to View Details", parent=root)
            return

        studentSeries = Series(self.studentDataFrame.loc[sid])
        studentSeries["Course Name"] = self.course[0]
        studentSeries["Year"] = self.course[1]

        student = Student(student_series=studentSeries)
        student.show_details_window()
