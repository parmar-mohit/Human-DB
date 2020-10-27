import datetime
import threading

lock = threading.Lock()


def write_log(message: str):
    # takes an string and writes that string on console and in log.txt file with date and time
    dateTime = datetime.datetime.now().strftime(
        "%d/%m/%y %H:%M:%S")  # getting current date and time in the specifies format
    dateTime = "(" + str(dateTime) + ") "  # enclosing the current datetime inside parenthesis to write in log
    toWrite = dateTime + message
    lock.acquire()  # acquiring lock so that 2 or more log messages from differrent thread do not overwrite
    fileWrite = open("log.txt", "a")  # opening file to write log in append mode
    print(toWrite)
    fileWrite.write(toWrite + "\n")
    lock.release()  # releasing lock so that other threads can acquire
    fileWrite.close()
