from tkinter import Toplevel

from PIL import ImageTk
from pandas import Series

from Assets.Classes.StudentFrame import StudentFrame
from Assets.file_func import get_file, save_file


class Student:
    def __init__(self, student_series: Series = None, sid: str = None, coursename: str = None, year: int = 0):

        if student_series is None:
            studentDataFrame = get_file("Courses/" + coursename + "/" + coursename + "_" + str(year) + ".DF")
            student_series = studentDataFrame.loc[sid]
            self.course = coursename
            self.year = year
        else:
            self.course = student_series["Course Name"]
            self.year = student_series["Year"]

        self.sid = student_series.name
        self.firstname = student_series["First Name"]
        self.lastname = student_series["Last Name"]
        self.fathername = student_series["Father Name"]
        self.mothername = student_series["Mother Name"]
        self.dob = student_series["DOB"]
        self.gender = student_series["Gender"]
        self.phoneNo = student_series["Phone No"]
        self.parentPhoneNo = student_series["Parent Phone No"]
        self.email = student_series["Email"]
        self.parentEmail = student_series["Parent Email"]
        self.address = student_series["Address"]
        self.rollNo = student_series["Roll No"]
        self.image = student_series["Image"]
        self.signImage = student_series["Sign Image"]

    def add_attendance_dataframe(self):
        attendanceDataFrame = get_file("Courses/" + self.course + "/Attendance_" + str(self.year) + ".DF")
        attendanceDataFrame[self.sid] = "N/A"
        save_file("Courses/" + self.course + "/Attendance_" + str(self.year) + ".DF", attendanceDataFrame)

    def show_details_window(self):
        root = Toplevel()
        root.title(self.sid)
        root.iconbitmap("Images/iconbitmap.ico")

        studentDetailsFrame = StudentFrame(root, entry=False)

        # configuring personalDetailsFrame
        studentDetailsFrame.firstnameLabel.config(text=self.firstname)
        studentDetailsFrame.lastnameLabel.config(text=self.lastname)
        if self.fathername is None:
            studentDetailsFrame.fathernameLabel.config(text="No Details available")
        else:
            studentDetailsFrame.fathernameLabel.config(text=self.fathername)

        if self.mothername is None:
            studentDetailsFrame.mothernameLabel.config(text="No Details available")

        else:
            studentDetailsFrame.mothernameLabel.config(text=self.mothername)

        studentDetailsFrame.dobLabel.config(text=str(self.dob))
        studentDetailsFrame.genderLabel.config(text=self.gender)

        # configuring contactDetailsFrame
        studentDetailsFrame.phoneLabel.config(text=self.phoneNo)
        if self.email is None:
            studentDetailsFrame.emailLabel.config(text="No Details available")
        else:
            studentDetailsFrame.emailLabel.config(text=self.email)

        studentDetailsFrame.parentPhoneLabel.config(text=self.parentPhoneNo)
        if self.parentEmail is None:
            studentDetailsFrame.parentEmailLabel.config(text="No Details Available")
        else:
            studentDetailsFrame.parentEmailLabel.config(text=self.parentEmail)

        # configuring addressFrame
        studentDetailsFrame.addressLabel.config(text=self.address["address"])
        studentDetailsFrame.cityLabel.config(text=self.address["city"])
        studentDetailsFrame.stateLabel.config(text=self.address["state"])
        studentDetailsFrame.pincodeLabel.config(text=self.address["pincode"])

        # configuring academicDetailsFrame
        studentDetailsFrame.courseLabel.config(text=self.course)
        studentDetailsFrame.yearLabel.config(text=str(self.year))
        studentDetailsFrame.sidLabel.config(text=self.sid)
        studentDetailsFrame.rollLabel.config(text=self.rollNo)

        # configuring images
        self.tkinterImage = ImageTk.PhotoImage(self.image)
        studentDetailsFrame.imageLabel.config(image=self.tkinterImage)
        self.tkinterSignImage = ImageTk.PhotoImage(self.signImage)
        studentDetailsFrame.signImageLabel.config(image=self.tkinterSignImage)

        # placing frame
        studentDetailsFrame.grid(row=0, column=0, padx=5, pady=5)

        root.mainloop()

    def update_dataframe(self):
        studentSeries = Series(name=self.sid)
        studentSeries["First Name"] = self.firstname
        studentSeries["Last Name"] = self.lastname
        studentSeries["Father Name"] = self.fathername
        studentSeries["Mother Name"] = self.mothername
        studentSeries["DOB"] = self.dob
        studentSeries["Gender"] = self.gender
        studentSeries["Phone No"] = self.phoneNo
        studentSeries["Parent Phone No"] = self.parentPhoneNo
        studentSeries["Email"] = self.email
        studentSeries["Parent Email"] = self.parentEmail
        studentSeries["Address"] = self.address
        studentSeries["Roll No"] = self.rollNo
        studentSeries["Image"] = self.image
        studentSeries["Sign Image"] = self.signImage

        studentDataFrame = get_file("Courses/" + self.course + "/" + "Student_" + str(self.year) + ".DF")

        if self.sid in studentDataFrame.index:
            studentDataFrame.drop(self.sid, inplace=True)

        studentDataFrame = studentDataFrame.append(studentSeries)

        save_file("Courses/" + self.course + "/" + "Student_" + str(self.year) + ".DF", studentDataFrame)
