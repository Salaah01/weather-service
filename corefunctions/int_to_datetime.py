"""Converts the integer representation of datetime (YYYYMMDDHHMM) into a
datetime object.
"""

# IMPORTS
# Python Core Imports
from datetime import datetime

# Third Party Imports

# Local Imports


def int_to_datetime(dateInt):
    """Converts dateInt where dateInt is an integer/string representing
    date and time in the format YYYYMMDDHHMM to a datetime object.
    """
    dateInt = str(dateInt)
    year = int(dateInt[:4])
    month = int(dateInt[4:6])
    day = int(dateInt[6:8])
    hour = int(dateInt[8:10])
    minute = int(dateInt[10:12])

    return datetime(year, month, day, hour, minute)


if __name__ == "__main__":
    print(
        int_to_datetime(202001010400) == datetime(2020, 1, 1, 4)
    )
