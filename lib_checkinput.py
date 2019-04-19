import datetime


def date(string):
    format = "%Y-%m-%d"
    try:
        datetime.datetime.strptime(string, format)
        return True
    except ValueError:
        return False


def time(string):
    format = "%H:%M:%S"
    try:
        datetime.datetime.strptime(string, format)
        return True
    except ValueError:
        return False
