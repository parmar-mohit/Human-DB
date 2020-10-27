# Human DB

## About

Human DB is a Database Management Application consisting of 2 programs, Sever Program and Client Program.Program is Designed to be used by educational institutes for storing information about their students as and when required.

### Program User

To use the Application or to perform certain task ,you must create a user.User can be Created from client program the option too create user appears on screen on when login window for client program is displayed. To create user you must enter your firstname,lastname create a new username and set a new password.user will now be created. Every user has read/write Permission.you can perform task only if you have required permission. When a new user is created it has no permission, however admin user can change this permission from server program. 

### Server Program

Server Program is responsible to systematically store data and to give it user as and when requested.Server Program can only be accessed by admin user other user cannot access Sever Program.Server Program has limited functionality. It is a MultiThreaded program which consist of n + 2 thread where n is no of clients connected

Task admin user can perform using server program are
* Add new Course
* Edit Read/Write Permission for existing course
* Delete a Course
* View Details of Currently Connected Client Program
* Force to Close Connection With a Client Program
* View Details of all User
* Delete Details of a Particular User(Except for admin,admin user Details cannot be Deleted)
* Stop Server while still running server program and perform some of the above mentioned task
* Stop Server and close Server Program

#### Exit Codes for Server Program

##### Exit Code 1

The Program was closed because there was problem binding socket to Ip Address and port

##### Exit Code 2

The Program was closed because socket was not created

##### Exit Code 3

The Progam was closed by user while in login window

### Client Program

Client Program is used to store new data,read/update existing data or delete existing data.Client Program does not store any data instead it request server program to send data.Client program is accessable by any valid user, However to store,read/update/delete data user must have the required permission.

Task that can be performed by a user using client program are
* View Details of Student
* Edit Details of a Student
* Delete Details of a Student
* View Attendance of Student on Specific Date
* Add Attendace Details for a Specific Date
* Change Username for user
* Change Password for user

---

## Naming Convention

* Variables are named using camelcase with firstletter as lowercase( Eg camelCase )
* Function  and function arguments are named using lowercase letters only and using underscore between 2 words( Eg hello_world )
* Classes are named using camelcase with firstletter as uppercase(Eg CamelCase )
* If file contains classes they file is named using same naming conventionas class
* If File contains function file is named using same naming convention as function

## File Structure

* Program Executable File
* Images Directory
* Courses
    * Course.DF
    * Com_Sci
        * Attendance_1.DF
        * Attendance_2.DF
        * Attendance_3.DF
        * Attendance_4.DF
        * Student_1.DF
        * Student_2.DF
        * Student_3.DF
        * Student_4.DF
    * Other_Courses
* .Users 

The Above exaplins the file structure for program in the directory where you have the executable file, you also have Images Directory where all the Images are stored.

Then we have Courses Directory, the Courses directory which contains Course.DF(DataFrame) which contains the a Pandas DataFrame storinf information about various course offered by institute.The Dataframe has coursename as index and consists of 2 other columns namely intake per year for that course and no of years in course.

Example for Course.DF

|            | Intake | Year |
|------------|--------|------|
| Com_Sci    | 120    |   4  |
| I.T        | 60     |   4  |
| Mechanical | 120    |   4  | 


Courses directory also contains subdirectories named after the courses offered in the above data Com_Sci subdirectory is stored, the Com_Sci subdirectory contans 2n files where n is the number of years in course the file is named as Student followed by a underscore followed by the year for which data is stored these files too contains pandas DataFrame with SID of Student as index and columns which are First Name,Last Name,Roll No,Father Name,Date of Birth,Gender,Phone No,Parent Phone No,Email,Parent Email,Address with street name,city ,state and pincode.

Example for Course_Year.DF

|     | First Name | Last Name | Roll No |
|-----|------------|-----------|---------|
| 415 |    Virat   |   Kohli   |     1   |

Other Files in Com_Sci subdirectory include Attendance Files which are named as Attendance followed by underscore followed by year with .DF Extension. As the name suggest these files are used to store attendance data of students.These files too contain Pandas Dataframe with date objects as index and sid as columns.This Dataframe contains boolean True or False as its value where True represents Present and False represents Absent

Example for Attendance_Year.DF

|            |  415  |  416 |  417  |
|------------|-------|------|-------|
| 2020-03-01 | True  | True | False |
| 2020-03-02 | False | True |  True |
| 2020-03-03 | True  | True |  True |

Back to Program directory, the program directory contains one important file .Users file similar to other files .Users file store Pandas DataFrame for storing data user.Dataframe has Username as index,other columns in dataframe are First Name,Last Name,Last Login Date,Last Logout Date. When a new Course is Created a new column for new course which contains a tuple for read/Write Permission

Example for .Users

|       | First Name | Last Name | Last Login Date |
|-------|------------|-----------|-----------------|
| admin |    admin   |   admin   |    06-10-2020   |

Note -  All the files are seriealised using pickle and then stored in binary mode instead of text mode

---

## Classes

### ClientConnection

ClientConnection Class Store the following attributes
* A socket object (Client Socket)
* Address of Client
* Server Socket Object
* A User Object if the program user has Logged In from Client Program

#### closer_connection

close_connection method takes one optional send_message arguement  default is false,f send_message is set to true the socket first send the message to client to close connection then it closes the socket.

### ClientSocket

ClientSocket class is responsiblr for communicating with server program from client Side.ClientSocket Class extends socket class from socket module

it has one messages attribute which is a list which contains all the messages recieved by socket, that are yet to be processed

#### connect_server

connec_server method takes on argument which should be a string which is the ip address of server. It tries to connect to server at specified ip address and port 5432

#### receive_message

It receives message from server and stores them in messages list

#### get message

get_message method takes one argument which is a integer which should be the request no for the message and return message if it is available in messages list ,if message is not received it will wait till it receives message and then return message

### Course Class

Course Class has follwing attributes
* Coursename 
* Intake per Year of Course
* No of Years in Course

#### Course Contructor

Course contructor can takes a Series using which it initialise the attributes or it can intialise attributes by just using coursename by reading data from Course.DF DataFrame

#### add_dataframe

add_dataframe method adss the details of respective course class to Courses/Course.DF DataFrame

#### make_directories

make_directories method creates a subdirectory named as coursename in course subdirectory and then creates necessary files in that subdirectory

#### delete_course

delete_course method is used when we want to details of the course. It first removes details from Course.DF File then it removes Details from .Users File then it deletes the respective Course Directory

#### update_permission

update_permission method takes a pandas Series with username as key and a tuple containing 2 boolean value ,first one for read permission and second one for write permission. It then adds/updates the columns for that coursename in .Users file with the given Series

### DateEntry Class

DateEntry Class extends ttk.Frame Class. It is used for input of a date

#### DateEntry Constructor

DateEntry Constructor takes a parent argument which is the parent widget of Frame.

#### get 

get method return None if no or improper date in entered else return a date object

#### set

set method takes a date object ar argument and sets the input field as the given date

### Listbox Class

Listbox Class creates an object similar to tkinter Listbox,but actually it is just a Treeview Object configured to perform as Listbox.This Class extends ttk.Frame Class and has only 2 attributes a treeview object and an scrollbar for that object

#### Listbox Constructor

Listbox Constructor takes parent,heading,height,width as argument and then create a treeview object based on given arguments along with a acrollbar

#### delete_selected

delete_selected removes the selectes item from listbox

#### delete_all

delete_all method removes all the node from treeview

#### get

get method returns the selected treeview node

#### insert

insert method takes one str arguments and then inserts that argument at the end of treeview

### Message Class

Message Class is a class that is used to communicate between client and server program

It has 4 attributes
* type
* action
* info
* request

type can be either request,response,order
if it is request then the program must send a response
if it is order then the program must perform certain predefined task

action tells which predefined task to do or what data to send as response

info contains data that may be required for doing pre-defined task or it conatins data if message type is response

request is just an integer which is used to check whether the response received is of the same request which was sent

### ServerSocket Class

ServerSocket Class extends socket.socket class has an acceptConnection attribute which is a bool variable and an connected attribute which is a dictionary with addr of client as key and client object as value

#### accept_connections

accept_connections method runs in a loop and accepts client connections only if acceptConnection attribute is set to True

#### close_all_conections

This method closes all connection with client

### Student Class

Student Class Stores the following data
* Full Name of Student
* Parent's Name
* Date of Birth and Gender
* Students Phone No and Parent's Phone No
* Students Email id and Parent's Email id
* Address in form of dictionary with address,city,state and pincode as key
* Course and Year of Student
* SID of Student
* Students Image and Sign Image

Note - Parent's Name and email id are optional fields so they may conatin None

#### Student Constructor

Student Class Constructor can take 1 argument which is a Series Object, using this series it can intialise all attributes, or it an take 3 attributes which are sid, coursename , year using which they can initialise attribute by getting details from DataFrame

#### add_attendance_dataframe

add_attendance_dataframe method is used to add column for newly created student in attendace file

#### show_details_window

show_details_window method creates a new window and displays all the info available about the student

#### update_dataframe

update_dataframe method first creates a pandas series and then uses that series to update the dataframe with new values for that course, 

### StudentFrame Class 

StudentFrame Class extends ttk.Frame Class.StudentFrame Class is used in displaying details of a student or it is used as input medium for getting details of student

#### StudentFrame Constructor

StudentFrame Constructor has 3 arguments parent, entry and write_permission, when entry is set to true the object of this class is to be used as input medium for getting details of student also when entry is set to True it also requires write_permission variable which should be a dictionary with coursename as key and no of years in course as value,it should only contain coursenames for which user is having write Permission set to True.When entry is set to True it does not require write_permission and the object is used to display details of student

### User Class

User class has follwing attributes

* First Name of User
* Last Name of User
* username of User
* Hashed Password of User
* Last Login Date with Time
* Last Logout Date with Time

#### User Constructor

User constructor can initialise varible using 2 methods either by passing a user_series which contains all values or by passing a username, which will then get data from .Users file dataframe

#### add_dataframe

add_dataframe method adds the data of a user to .Users DataFrame

#### update_login_date and update_logout date

The above 2 methods is used to update the login and logout attributes as well as making changes in .Users DataFrame

#### password_check

password_check is a static method which checks if the given input which is a password , that mets the required criteria it returns True if the password has an uppercase letter, a lowercase letter and a number

#### password_hash

password_hash is a staticemethod that uses sha256 algorithm to convert given input which is a password to hashed value and return the hashed 

#### username_check

username_check is a static method which checks if given input has an white space or a special character. It returns True if input has an white space or has an Special Character other than underscore. OtherWise it returns False

## Action Codes

### Action Code for Server Program

#### Action code 1

Close Connection with Client

#### Action code 2 

Request user DataFrame

#### Action code 3

Adds new User to User DataFrame. Info attribute of message has user object

#### Action code 4

User logged in from client program. Info attributes contains user object

#### Action code 5

Change Password for particular user. Info attribute contains a tuple containing username of user and a new hashed password

#### Action code 6

Requesting course DataFrame

#### Action Code 7

Requesting to add new student

It Should reponsond by giving a message with a status number in info attribute

##### Status Number 1

Student was not added because student with same sid Exist in database

##### Status Number 2

Student Was not added to Database because intake for that course and year was full

##### Status Number 3

Student was added to database successfully

#### Action Code 8

Request Student DataFrame for course. Info attribute contains a tuple containing course and year

#### Action Code 9

Delete a Student. Info attributes contains a tuple containing sid,course,year of student

#### Action Code 10

Add attendance. Info attribute contains a tuple containing course,year and series with name as date, sid as key and true or false(present or absent) as value.If attendnace already exist for that date it will overwrite


#### Action Code 11

Request attendance Dataframe. Info Attribute contains a tuple with course and year

### Action code for Client Program

#### Action code 1

Close Connection with Server