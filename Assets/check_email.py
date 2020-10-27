# copied from geeksforgeeks.org

# checks if the email entered is valid

import re

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def check_email(email: str) -> bool:
    if re.search(regex, email):
        return True
    else:
        return False
