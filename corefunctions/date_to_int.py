"""Converts a datetime object to an integer in the format YYYYMMDDHHMM"""


def date_to_int(inputDate):
    """Converts intputDate into an integer in the format YYYYMMDDHHMM where
    inputDate is a datatime object.
    """
    return int(inputDate.strftime('%Y%m%d%H%M'))
