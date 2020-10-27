from pickle import load, dump

from pandas import DataFrame


def get_file(file_path: str) -> DataFrame:
    # opens file the specified by path in read mode and returns its content
    fileRead = open(file_path, "rb")
    data = load(fileRead)
    fileRead.close()
    return data


def save_file(file_path: str, data: DataFrame):
    # opens the file specified by path in write mode
    # and writes fil with specified data
    fileWrite = open(file_path, "wb")
    dump(data, fileWrite)
    fileWrite.close()
