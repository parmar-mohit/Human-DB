from os import system

from pandas import Series, DataFrame

from Assets.file_func import get_file, save_file


class Course:
    def __init__(self, course_series: Series = None, coursename: str = None):
        if course_series is None:
            courseDataFrame = get_file("Courses/Course.DF")
            course_series = courseDataFrame.loc[coursename]

        self.coursename = str(course_series.name)
        self.intake = course_series["Intake"]
        self.year = course_series["Year"]

    def add_dataframe(self):
        courseDataFrame = get_file("Courses/Course.DF")
        if self.coursename in courseDataFrame.index:
            courseDataFrame.drop(self.coursename, inplace=True)
        courseDataFrame = courseDataFrame.append(
            Series({"Intake": self.intake, "Year": self.year}, name=self.coursename))
        save_file("Courses/Course.DF", courseDataFrame)

    def delete_course(self):
        courseDataFrame = get_file("Courses/Course.DF")
        courseDataFrame.drop(self.coursename, inplace=True)
        save_file("Courses/Course.DF", courseDataFrame)

        userDataFrame = get_file(".Users")
        del userDataFrame[self.coursename]
        save_file(".Users", userDataFrame)

        system("rmdir /S /Q Courses\\" + self.coursename)

    def make_directories(self):
        system("mkdir Courses\\" + self.coursename)
        df = DataFrame()
        for i in range(1, self.year + 1):
            save_file("Courses/" + self.coursename + "/Attendance_" + str(i) + ".DF", df)
            save_file("Courses/" + self.coursename + "/Student_" + str(i) + ".DF", df)

    def update_permission(self, permission_series: Series):
        userDataFrame = get_file(".Users")
        userDataFrame[self.coursename] = permission_series
        save_file(".Users", userDataFrame)

    @staticmethod
    def coursename_check(coursename: str):
        for i in range(len(coursename)):
            if coursename[i].isspace():
                coursename = coursename[:i] + "_" + coursename[i + 1:]

        return coursename
