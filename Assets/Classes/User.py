from datetime import date
from hashlib import sha256

from pandas import Series

from Assets.file_func import get_file, save_file


class User:
    def __init__(self, user_series: Series = None, username: str = None):
        if user_series is None:
            userDataFrame = get_file(".Users")
            user_series = userDataFrame.loc[username]
            self.password = user_series["Password"]
        else:
            self.password = self.password_hash(user_series["Password"])

        self.username = user_series.name
        self.firstname = user_series["First Name"]
        self.lastname = user_series["Last Name"]
        self.loginDateTime = user_series["Last Login Date"]
        self.logoutDateTime = user_series["Last Logout Date"]
        self.dbPermission = user_series[5:]
        if self.dbPermission is None:
            self.dbPermission = {}

    def add_dataframe(self):
        userDataFrame = get_file(".Users")
        if self.username in userDataFrame.index:
            userDataFrame.drop(self.username, inplace=True)
        userSeries = Series({"First Name": self.firstname,
                             "Last Name": self.lastname,
                             "Password": self.password,
                             "Last Login Date": self.loginDateTime,
                             "Last Logout Date": self.logoutDateTime}, name=self.username)
        try:
            userSeries.append(self.dbPermission)
        except:
            pass
        userDataFrame = userDataFrame.append(userSeries)
        save_file(".Users", userDataFrame)

    def update_login_date(self, date_obj: date):
        self.loginDateTime = date_obj
        userDataFrame = get_file(".Users")
        userDataFrame.loc[self.username, "Last Login Date"] = date_obj
        save_file(".Users", userDataFrame)

    def update_logout_date(self, date_obj: date):
        self.logoutDateTime = date_obj
        userDataFrame = get_file(".Users")
        userDataFrame.loc[self.username, "Last Logout Date"] = date_obj
        save_file(".Users", userDataFrame)

    @staticmethod
    def password_check(password: str):
        check_list = [False, False, False]
        # uppercase, lowercase, number

        for char in password:
            if char.isupper():
                check_list[0] = True

            if char.islower():
                check_list[1] = True

            if char.isnumeric():
                check_list[2] = True

            if not (False in check_list):
                return True

        return False

    @staticmethod
    def password_hash(password: str) -> str:
        hash = sha256()
        hash.update(password.encode())
        return hash.hexdigest()

    @staticmethod
    def username_check(username: str):
        for char in username:
            if char.isspace() or (not char.isalnum() and char != "_"):
                return True
        return False
