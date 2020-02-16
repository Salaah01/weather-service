"""Unittests for the corefunctions.unit_conversion.UnitConversion class.
Tests will test that each type of unit is converted as expected and where
applicable raise an exception.

Included tests:
    * test_convert_temperature
"""

# IMPORTS
# Python Core Imports
import unittest

# Third Party Imports

# Local Imports
from .convert_date_string_testcases import testcases as convertDateStringTests
from .convert_temperature_testcases import testcases as convertTemperatureTests


class TestUnitConversion(unittest.TestCase):
    """Tests each method in the UnitConversion class.
    Empty class object where test generators will be used to build the class
    with tests.
    """


def base_test(actualResult, expectedResult, failMessage=None):
    """Function yielding a sub-function to check if a test has passed."""

    def test(self):
        self.assertEquals(actualResult, expectedResult, failMessage)
    return test


def convert_date_string_test_generator():
    """Generates tests to be attached to the TestUnitConversion.
    These tests will check that the convert_date_string method is able convert
    dates in various to a datetime object and a integer in the format
    YYYYMMDDHHMM correctly. The test will check that the method handle the
    following forwards:
        * YYYY-MM-DD
        * YYYY-MM-DDTHH:MM:SSZ
        * YYYYMMDDTHHMMSSZ
        * YYYY-MM-DDTHH:MM:SS+HH:SS
    """

    # Add testcases to TestUnitConversion
    for idx, testcase in enumerate(convertDateStringTests):
        setattr(
            TestUnitConversion,
            f'test_convert_date_string_{idx}',
            base_test(testcase['actual'], testcase['expected'])
        )


def convert_temperature_test_generator():
    """Generates tests to be attached to the TestUnitConversion.
    These tests will check that the convert_temperature method is able convert
    units correctly. The test will check the following conversions are done
    correctly:
        * Kelvin (K) to Celsius (C)
        * Celsius (C) to Kelvin (K)
    """

    # Add testcases to TestUnitConversion
    for idx, testcase in enumerate(convertTemperatureTests):
        setattr(
            TestUnitConversion,
            f'test_convert_date_string_{idx}',
            base_test(
                testcase['actual'],
                testcase['expected'],
                testcase['failMessage']
            )
        )


convert_date_string_test_generator()
convert_temperature_test_generator()
