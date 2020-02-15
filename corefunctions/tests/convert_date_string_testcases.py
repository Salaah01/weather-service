"""Test cases for test_unit_conversion.UnitConversion.
Used by the test_convert_date_string_generator to build the iteratively
add tests to the main test class.
"""

# IMPORTS
# Python Core Imports
from datetime import datetime

# Third Party Imports

# Local Imports
from corefunctions import UnitConversion


testcases = [
    {
        'actual': UnitConversion('2020-02-15',
                                 'unknown',
                                 'datetime').convert_date_string(),
        'expected': datetime(2020, 2, 15, 0, 0, 0)
    },
    {
        'actual': UnitConversion('2020-02-15',
                                 'unknown',
                                 'int').convert_date_string(),
        'expected': 202002150000
    },
    {
        'actual': UnitConversion('2017-01-01T11:22:33Z',
                                 'unknown',
                                 'datetime').convert_date_string(),
        'expected': datetime(2017, 1, 1, 11, 22, 33)
    },
    {
        'actual': UnitConversion('2017-01-01T11:22:33Z',
                                 'unknown',
                                 'int').convert_date_string(),
        'expected': 201701011122
    },
    {
        'actual': UnitConversion('2020-02-15T20:53:15+03:02',
                                 'unknown',
                                 'datetime').convert_date_string(),
        'expected': datetime(2020, 2, 15, 23, 55, 15)
    },
    {
        'actual': UnitConversion('2020-02-15T20:53:15+03:02',
                                 'unknown',
                                 'int').convert_date_string(),
        'expected': 202002152355
    },
    {
        'actual': UnitConversion('2020-02-15T20:53:15-03:02',
                                 'unknown',
                                 'datetime').convert_date_string(),
        'expected': datetime(2020, 2, 15, 17, 51, 15)
    },
    {
        'actual': UnitConversion('2020-02-15T20:53:15-03:02',
                                 'unknown',
                                 'int').convert_date_string(),
        'expected': 202002151751
    },
    {
        'actual': UnitConversion('20170101T112233Z',
                                 'unknown',
                                 'datetime').convert_date_string(),
        'expected': datetime(2017, 1, 1, 11, 22, 33)
    },
    {
        'actual': UnitConversion('20170101T112233Z',
                                 'unknown',
                                 'int').convert_date_string(),
        'expected': 201701011122
    },
]
