"""Unittests for the corefunctions.unit_conversion.UnitConversion class.
Tests will test that each type of unit is converted as expected and where
applicable raise an exception.

Included tests:
    * test_convert_temperature
"""

# IMPORTS
# Python Core Imports
import unittest
from datetime import datetime

# Third Party Imports

# Local Imports
import corefunctions
from .convert_date_string_testcases import testcases as convertDateStringTests


class TestUnitConversion(unittest.TestCase):
    """Tests each method in the UnitConversion class."""

    def test_convert_temperature(self):
        """Tests the convert temperature method."""

        # Each item in testcases is a tuple of size 2, where the first element
        # in the tuple is the actual result and the second element is the
        # expected result.
        testcases = [
            (
                corefunctions.UnitConversion(
                    99, 'K', 'C').convert_temperature(),
                -174.15
            ),
            (
                corefunctions.UnitConversion(
                    99, 'K', 'C', 1, True).convert_temperature(),
                '-174.1C'
            )
        ]

        for testcase in testcases:
            self.assertEquals(testcase[0], testcase[1])


def base_test(actualResult, expectedResult, failMessage=None):
    """Function yielding a sub-function to check if a test has passed."""

    def test(self):
        self.assertEquals(actualResult, expectedResult, failMessage)
    return test


def test_convert_date_string_generator():
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


test_convert_date_string_generator()
