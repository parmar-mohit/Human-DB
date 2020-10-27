from datetime import datetime

from Assets.Classes.Message import Message
from Assets.file_func import get_file, save_file
from Assets.write_log import write_log


def close_connection(message, client_connection):
    client_connection.close_connection()


def request_user_dataframe(message, client_connection):
    userDataFrame = get_file(".Users")
    message = Message("response", None, userDataFrame, message.request)
    client_connection.socket.send(message.encode())
    if client_connection.user is None:
        write_log("User Dataframe sent to " + str(client_connection.addr))
    else:
        write_log("User Dataframe sent to " + client_connection.user.username + " at " + str(client_connection.addr))


def add_new_user(message, client_connection):
    user = message.info
    user.add_dataframe()
    write_log("New user with username {} added from {}".format(user.username, str(client_connection.addr)))


def user_login(message, client_connection):
    user = message.info
    user.update_login_date(datetime.now())
    client_connection.user = user
    write_log(user.username + " User logged in from client Program at " + str(client_connection.addr))


def change_password(message, client_connection):
    client_connection.user.password = message.info[1]
    userDataFrame = get_file(".Users")
    userDataFrame.loc[message.info[0], "Password"] = message.info[1]
    save_file(".Users", userDataFrame)
    write_log("Password Changed for " + message.info[0])


def request_course_dataframe(message, client_connection):
    courseDataFrame = get_file("Courses/Course.DF")
    message = Message("response", None, courseDataFrame, message.request)
    client_connection.socket.send(message.encode())
    if client_connection.user is None:
        write_log("Course Dataframe sent to " + str(client_connection.addr))
    else:
        write_log("Course Dataframe sent to " + client_connection.user.username + " at " + str(client_connection.addr))


def add_student(message, client_connection):
    student = message.info

    courseDataFrame = get_file("Courses/Course.DF")
    for coursename in courseDataFrame.index:
        for i in range(1, int(courseDataFrame.loc[coursename, "Year"] + 1)):
            path = "Courses/{}/Student_{}.DF".format(coursename, str(i))
            df = get_file(path)
            if student.sid in df.index:
                message = Message("response", None, 1, message.request)
                client_connection.socket.send(message.encode())
                write_log("Student requested to add from {} was not added to database,Status 1".format(
                    str(client_connection.user.username)))
                return

    path = "Courses/{}/Student_{}.DF".format(student.course, str(student.year))
    studentDataFrame = get_file(path)
    if studentDataFrame.shape[0] >= int(courseDataFrame.loc[student.course, "Intake"]):
        message = Message("response", None, 2, message.request)
        client_connection.socket.send(message.encode())
        write_log("Student request to add from {} was not added to database,Status 2".format(
            str(client_connection.user.username)))
        return

    student.update_dataframe()
    student.add_attendance_dataframe()
    message = Message("response", None, 3, message.request)
    client_connection.socket.send(message.encode())

    write_log("Student Added to database with sid {} ,requested to add {}".format(student.sid,
                                                                                  str(client_connection.user.username)))


def student_dataframe(message, client_connection):
    course, year = message.info
    studentDataFrame = get_file("Courses/{}/Student_{}.DF".format(course, str(year)))
    message = Message("response", None, studentDataFrame, message.request)
    client_connection.socket.send(message.encode())
    write_log("{}_{} dataframe sent to {} at {}".format(course, year, client_connection.user.username,
                                                        str(client_connection.addr)))


def delete_student(message, client_connection):
    sid, course, year = message.info
    studentDataFrame = get_file("Courses/{}/Student_{}.DF".format(course, str(year)))
    studentDataFrame.drop(sid, inplace=True)
    save_file("Courses/{}/Student_{}.DF".format(course, str(year)), studentDataFrame)

    attendanceDataFrame = get_file("Courses/{}/Attendance_{}.DF".format(course, str(year)))
    del attendanceDataFrame[sid]
    save_file("Courses/{}/Attendance{}.DF".format(course, str(year)), attendanceDataFrame)

    write_log(
        "{} at {} deleted student with SID {}".format(client_connection.user.username, str(client_connection.addr),
                                                      sid))


def add_attendance(message, client_connection):
    course, year, series = message.info
    attendanceDataFrame = get_file("Courses/{}/Attendance_{}.DF".format(course, year))
    if series.name in attendanceDataFrame.index:
        attendanceDataFrame.drop(series.name, inplace=True)

    attendanceDataFrame = attendanceDataFrame.append(series)

    save_file("Courses/{}/Attendance_{}.DF".format(course, year), attendanceDataFrame)

    write_log("{} at {} added attendance for {} year {}".format(client_connection.user.username, client_connection.addr,
                                                                course, year))


def request_attendance_dataframe(message, client_connection):
    course, year = message.info
    attendanceDataFrame = get_file("Courses/{}/Attendance_{}.DF".format(course, year))
    message = Message("response", None, attendanceDataFrame, message.request)

    client_connection.socket.send(message.encode())
    write_log("{}_{} attendance dataframe sent to {}  at {}".format(course, year, client_connection.user.username,
                                                                    client_connection.addr))


serverAction = {
    1: close_connection,
    2: request_user_dataframe,
    3: add_new_user,
    4: user_login,
    5: change_password,
    6: request_course_dataframe,
    7: add_student,
    8: student_dataframe,
    9: delete_student,
    10: add_attendance,
    11: request_attendance_dataframe
}
