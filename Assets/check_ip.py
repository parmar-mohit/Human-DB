# copied program from geeksforgeeks.org

# checks whether ip address entered is valid

import re

regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''


# Define a function for
# validate an Ip addess
def check_ip(ip: str) -> bool:
    if re.search(regex, ip):
        return True
    else:
        return False
