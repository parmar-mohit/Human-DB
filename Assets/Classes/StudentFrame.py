from tkinter import ttk, StringVar, IntVar, filedialog
from PIL import Image, ImageTk
from Assets.Classes.DateEntry import DateEntry


class StudentFrame(ttk.Frame):
    def __init__(self, parent, entry: bool = True, write_permission: dict = None):
        def course_select(value):
            nonlocal academicDetailsFrame, write_permission
            self.yearOptionMenu = ttk.OptionMenu(academicDetailsFrame, self.yearIntVar, None,
                                                 *list(range(1, int(write_permission[value] + 1))))
            self.yearOptionMenu.grid(row=0, column=3, padx=5, pady=5)

        super().__init__(parent)
        self.parent = parent

        personalDetailsFrame = ttk.LabelFrame(self, text="Personal Details")
        contactDetailsFrame = ttk.LabelFrame(self, text="Contact Details")
        addressFrame = ttk.LabelFrame(self, text="Address")
        academicDetailsFrame = ttk.LabelFrame(self, text="Academic details")
        imageFrame = ttk.Frame(self)
        signImageFrame = ttk.Frame(self)

        personalDetailsFrame.grid(row=0, column=0, padx=5, pady=5)
        contactDetailsFrame.grid(row=1, column=0, padx=5, pady=5)
        addressFrame.grid(row=2, column=0, padx=5, pady=5)
        academicDetailsFrame.grid(row=3, column=0, padx=5, pady=5)
        imageFrame.grid(row=0, column=1, rowspan=3, padx=5, pady=5)
        signImageFrame.grid(row=3, column=1, padx=5, pady=5)

        if not entry:
            # creating and placing child widgets for personalDetailsFrame
            self.firstnameLabel = ttk.Label(personalDetailsFrame, justify="left")
            self.lastnameLabel = ttk.Label(personalDetailsFrame, justify="left")
            self.fathernameLabel = ttk.Label(personalDetailsFrame, justify="left")
            self.mothernameLabel = ttk.Label(personalDetailsFrame, justify="left")
            self.dobLabel = ttk.Label(personalDetailsFrame, justify="left")
            self.genderLabel = ttk.Label(personalDetailsFrame, justify="left")

            self.firstnameLabel.grid(row=0, column=1, padx=5, pady=5)
            self.lastnameLabel.grid(row=0, column=3, padx=5, pady=5)
            self.fathernameLabel.grid(row=1, column=1, padx=5, pady=5)
            self.mothernameLabel.grid(row=1, column=3, padx=5, pady=5)
            self.dobLabel.grid(row=2, column=1, padx=5, pady=5)
            self.genderLabel.grid(row=2, column=3, padx=5, pady=5)

            # creating and placing child widgets for contactDetailsFrame
            self.phoneLabel = ttk.Label(contactDetailsFrame, justify="left")
            self.emailLabel = ttk.Label(contactDetailsFrame, justify="left")
            self.parentPhoneLabel = ttk.Label(contactDetailsFrame, justify="left")
            self.parentEmailLabel = ttk.Label(contactDetailsFrame, justify="left")

            self.phoneLabel.grid(row=0, column=1, padx=5, pady=5)
            self.emailLabel.grid(row=0, column=3, padx=5, pady=5)
            self.parentPhoneLabel.grid(row=1, column=1, padx=5, pady=5)
            self.parentEmailLabel.grid(row=1, column=3, padx=5, pady=5)

            # creating and placing child widgets for addressFrame
            self.addressLabel = ttk.Label(addressFrame, justify="left")
            self.cityLabel = ttk.Label(addressFrame, justify="left")
            self.stateLabel = ttk.Label(addressFrame, justify="left")
            self.pincodeLabel = ttk.Label(addressFrame, justify="left")

            self.addressLabel.grid(row=0, column=1, padx=5, pady=5)
            self.cityLabel.grid(row=0, column=3, padx=5, pady=5)
            self.stateLabel.grid(row=1, column=1, padx=5, pady=5)
            self.pincodeLabel.grid(row=1, column=3, padx=5, pady=5)

            # creating and placing child widgets for academicDetailsFrame
            self.courseLabel = ttk.Label(academicDetailsFrame, justify="left")
            self.yearLabel = ttk.Label(academicDetailsFrame, justify="left")
            self.sidLabel = ttk.Label(academicDetailsFrame, justify="left")
            self.rollLabel = ttk.Label(academicDetailsFrame, justify="left")

            self.courseLabel.grid(row=0, column=1, padx=5, pady=5)
            self.yearLabel.grid(row=0, column=3, padx=5, pady=5)
            self.sidLabel.grid(row=1, column=1, padx=5, pady=5)
            self.rollLabel.grid(row=1, column=3, padx=5, pady=5)

            # creating and placing child widgets for imageFrame
            self.imageLabel = ttk.Label(imageFrame)
            self.imageLabel.grid(row=0, column=0, padx=5, pady=5)

            # creating and placing child widgets for signImageFrame
            self.signImageLabel = ttk.Label(signImageFrame)
            self.signImageLabel.grid(row=0, column=0, padx=5, pady=5)
        else:
            self.firstnameEntry = ttk.Entry(personalDetailsFrame)
            self.lastnameEntry = ttk.Entry(personalDetailsFrame)
            self.fathernameEntry = ttk.Entry(personalDetailsFrame)
            self.mothernameEntry = ttk.Entry(personalDetailsFrame)
            self.dobEntry = DateEntry(personalDetailsFrame)
            self.genderStringVar = StringVar()
            self.genderStringVar.set("N/A")
            self.genderOptionMenu = ttk.OptionMenu(personalDetailsFrame, self.genderStringVar, None, "Male", "Female",
                                                   "Other")

            self.firstnameEntry.grid(row=0, column=1, padx=5, pady=5)
            self.lastnameEntry.grid(row=0, column=3, padx=5, pady=5)
            self.fathernameEntry.grid(row=1, column=1, padx=5, pady=5)
            self.mothernameEntry.grid(row=1, column=3, padx=5, pady=5)
            self.dobEntry.grid(row=2, column=1, padx=5, pady=5)
            self.genderOptionMenu.grid(row=2, column=3, padx=5, pady=5)

            # creating and placing widgets for contactDetailsFrame
            self.phoneEntry = ttk.Entry(contactDetailsFrame)
            self.emailEntry = ttk.Entry(contactDetailsFrame, width=30)
            self.parentPhoneEntry = ttk.Entry(contactDetailsFrame)
            self.parentEmailEntry = ttk.Entry(contactDetailsFrame, width=30)

            self.phoneEntry.grid(row=0, column=1, padx=5, pady=5)
            self.emailEntry.grid(row=0, column=3, padx=5, pady=5)
            self.parentPhoneEntry.grid(row=1, column=1, padx=5, pady=5)
            self.parentEmailEntry.grid(row=1, column=3, padx=5, pady=5)

            # creating and placing child widgets for addressFrame
            self.addressEntry = ttk.Entry(addressFrame)
            self.cityEntry = ttk.Entry(addressFrame)
            self.stateEntry = ttk.Entry(addressFrame)
            self.pincodeEntry = ttk.Entry(addressFrame)

            self.addressEntry.grid(row=0, column=1, padx=5, pady=5)
            self.cityEntry.grid(row=0, column=3, padx=5, pady=5)
            self.stateEntry.grid(row=1, column=1, padx=5, pady=5)
            self.pincodeEntry.grid(row=1, column=3, padx=5, pady=5)

            # creating and placing child widgets for academicDetailsFrame
            self.courseStringVar = StringVar()
            self.courseOptionMenu = ttk.OptionMenu(academicDetailsFrame, self.courseStringVar, None,
                                                   *list(write_permission.keys()), command=course_select)
            self.yearIntVar = IntVar()

            self.sidEntry = ttk.Entry(academicDetailsFrame)
            self.rollEntry = ttk.Entry(academicDetailsFrame)

            self.courseOptionMenu.grid(row=0, column=1, padx=5, pady=5)
            self.sidEntry.grid(row=1, column=1, padx=5, pady=5)
            self.rollEntry.grid(row=1, column=3, padx=5, pady=5)

            # creating and placing child widgets for imageFrame
            fileReadPersonImage = open("Images/Person.jpg", "rb")
            image = Image.open(fileReadPersonImage)

            self.image = image.resize((120, 200), Image.ANTIALIAS)
            self.tkinterImage = ImageTk.PhotoImage(self.image)
            self.imageLabel = ttk.Label(imageFrame, image=self.tkinterImage)
            ttk.Button(imageFrame, text="Select Image", command=self.image_button_on_click).grid(row=1, column=0,
                                                                                                 padx=5, pady=5)

            self.imageLabel.grid(row=0, column=0, padx=5, pady=5)

            # creating and placing child widgets for signImageFrame
            fileRead = open("Images/signImage.jpg", "rb")
            image = Image.open(fileRead)

            self.signImage = image.resize((120, 55), Image.ANTIALIAS)
            self.tkinterSignImage = ImageTk.PhotoImage(self.signImage)
            self.signImageLabel = ttk.Label(signImageFrame, image=self.tkinterSignImage)
            signImageButton = ttk.Button(signImageFrame, text="Select Image", command=self.sign_image_button_on_click)

            self.signImageLabel.grid(row=0, column=0, padx=5, pady=5)
            signImageButton.grid(row=1, column=0, padx=5, pady=5)

        # creating and placing child widgets for personalDetailsFrame
        firstnameLabel = ttk.Label(personalDetailsFrame, text="First Name : ")
        lastnameLabel = ttk.Label(personalDetailsFrame, text="Last Name : ")
        fathernameLabel = ttk.Label(personalDetailsFrame, text="Father's Name* : ")
        mothernameLabel = ttk.Label(personalDetailsFrame, text="Mother's Name* : ")
        dobLabel = ttk.Label(personalDetailsFrame, text="Date of Birth : ")
        genderLabel = ttk.Label(personalDetailsFrame, text="Gender : ")

        firstnameLabel.grid(row=0, column=0, padx=5, pady=5)
        lastnameLabel.grid(row=0, column=2, padx=5, pady=5)
        fathernameLabel.grid(row=1, column=0, padx=5, pady=5)
        mothernameLabel.grid(row=1, column=2, padx=5, pady=5)
        dobLabel.grid(row=2, column=0, padx=5, pady=5)
        genderLabel.grid(row=2, column=2, padx=5, pady=5)

        # creating and placing details for contactDetailsFrame
        phoneLabel = ttk.Label(contactDetailsFrame, text="Phone No : ")
        emailLabel = ttk.Label(contactDetailsFrame, text="Email* : ")
        parentPhoneLabel = ttk.Label(contactDetailsFrame, text="Parent Phone No : ")
        parentEmailLabel = ttk.Label(contactDetailsFrame, text="Parent's Email* : ")

        phoneLabel.grid(row=0, column=0, padx=5, pady=5)
        emailLabel.grid(row=0, column=2, padx=5, pady=5)
        parentPhoneLabel.grid(row=1, column=0, padx=5, pady=5)
        parentEmailLabel.grid(row=1, column=2, padx=5, pady=5)

        # creating and placing child widgets for addressFrame
        addressLabel = ttk.Label(addressFrame, text="Address : ")
        cityLabel = ttk.Label(addressFrame, text="City : ")
        stateLabel = ttk.Label(addressFrame, text="State : ")
        pincodeLabel = ttk.Label(addressFrame, text="Pincode : ")

        addressLabel.grid(row=0, column=0, padx=5, pady=5)
        cityLabel.grid(row=0, column=2, padx=5, pady=5)
        stateLabel.grid(row=1, column=0, padx=5, pady=5)
        pincodeLabel.grid(row=1, column=2, padx=5, pady=5)

        # creating and placing child widgets for acacdemicDetailsFrame
        courseLabel = ttk.Label(academicDetailsFrame, text="Course : ")
        yearLabel = ttk.Label(academicDetailsFrame, text="Year : ")
        sidLabel = ttk.Label(academicDetailsFrame, text="SID : ")
        rollLabel = ttk.Label(academicDetailsFrame, text="Roll No : ")

        courseLabel.grid(row=0, column=0, padx=5, pady=5)
        yearLabel.grid(row=0, column=2, padx=5, pady=5)
        sidLabel.grid(row=1, column=0, padx=5, pady=5)
        rollLabel.grid(row=1, column=2, padx=5, pady=5)

    def image_button_on_click(self):
        imagePath = filedialog.askopenfile(parent=self.parent, initialdir="./", title="Select Image", filetypes=(
            ("JPEG Files", "*jpeg"), ("JPG Files", "*jpg"), ("PNG Files", "*png")))

        if imagePath == None:
            return

        fileRead = open(imagePath.name, "rb")
        image = Image.open(fileRead)

        self.image = image.resize((120, 200), Image.ANTIALIAS)
        self.tkinterImage = ImageTk.PhotoImage(self.image)
        self.imageLabel.config(image=self.tkinterImage)

    def sign_image_button_on_click(self):
        imagePath = filedialog.askopenfile(parent=self.parent, initialdir="./", title="Select Image", filetypes=(
            ("JPEG Files", "*.jpeg"), ("JPG Files", "*.jpg"), ("PNG Files", "*.png")))

        if imagePath == None:
            return

        fileRead = open(imagePath.name, "rb")
        image = Image.open(fileRead)

        self.signImage = image.resize((120, 55), Image.ANTIALIAS)
        self.tkinterSignImage = ImageTk.PhotoImage(self.signImage)
        self.signImageLabel.config(image=self.tkinterSignImage)
