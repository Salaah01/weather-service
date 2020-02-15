"""Converts the units of a value."""

# IMPORTS
# Python Core Imports
import re
from datetime import datetime, timedelta

# Third Party Imports

# Local Imports
from corefunctions import date_to_int


class UnitConversion:
    """Contains methods that will convert a value of a certain unit to
    another type of unit..
    Arguments:
        * value [int/float]: the value to convert
        * initialUnit [str]: the the units of the value
        * newUnit [str]: the unit to convert the value to.
        * maxPrecision [int]: (default=4) Python can produce a floating point
                              error working with decimals. After the
                              conversion, the value will be rounded to the
                              number defined as maxPrecision.
        * showUnits[bool]: (default=False) If set to True, the final value
                           will be converted into a string with the units
                           placed at the end of the string.
    """

    def __init__(
        self,
        value,
        initialUnit,
        newUnit,
        maxPrecision=10,
        showUnits=False
    ):
        self.value = value
        self.initialUnit = initialUnit
        self.newUnit = newUnit
        self.maxPrecision = maxPrecision
        self.showUnits = showUnits

    def convert_temperature(self):
        """Converts temperatures to new units."""
        converted = False
        if self.initialUnit == 'K' and self.newUnit == 'C':
            convertedValue = round(self.value - 273.15, self.maxPrecision)
            converted = True

        if converted:
            if self.showUnits:
                return f'{convertedValue}{self.newUnit}'
            else:
                return convertedValue

        else:
            raise ValueError(
                f'temperature convert of {self.initialUnit} to {self.newUnit} \
                is not supported.'
            )

    def convert_date_string(self):
        """Converts date strings to a new format.
        Can also handle unknown formats where the method will be able to
        read the value which are in ISO-8601 formats or are in the format
        YYYY-MM-DD.
        """
        converted = False

        if self.initialUnit == 'unknown':

            # example pattern: 2020-02-15
            if re.match('^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$', self.value):
                datetimeVal = datetime.strptime(self.value, '%Y-%m-%d')

            # example pattern: 2017-01-01T00:00:00Z
            elif re.match(
                '^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])T(([01]\d)|2[0-3]):(([0-5]\d)):(([0-5]\d)))Z$',
                self.value
            ):
                datetimeVal = datetime.strptime(
                    self.value,
                    '%Y-%m-%dT%H:%M:%SZ'
                )

            # example pattern: 2020-02-15T20:53:15+00:00
            elif re.match(
                '^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])T(([01]\d)|2[0-3]):(([0-5]\d)):(([0-5]\d))[+-](([0-5]\d)):(([0-5]\d)))$',
                self.value
            ):
                timeSection = datetime.strptime(
                    self.value[0:-6], '%Y-%m-%dT%H:%M:%S')
                tzAddHours = self.value[-6] == '+'
                tzHours = int(self.value[20:22])
                tzMins = int(self.value[23:])

                if tzAddHours:
                    datetimeVal = timeSection + \
                        timedelta(hours=tzHours, minutes=tzMins)
                else:
                    datetimeVal = timeSection - \
                        timedelta(hours=tzHours, minutes=tzMins)

            # pattern example: 20200215T205315Z
            elif re.match(
                '^([12]\d{3}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])T(([01]\d)|2[0-3])(([0-5]\d))(([0-5]\d)))Z$',
                self.value
            ):
                datetimeVal = datetime.strptime(self.value, '%Y%m%dT%H%M%SZ')

            else:
                raise ValueError(
                    'Could not find datetime in the string provided.')

            if self.newUnit == 'datetime':
                return datetimeVal
            elif self.newUnit == 'int':
                return date_to_int(datetimeVal)
