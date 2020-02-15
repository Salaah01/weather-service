"""Converts the units of a value."""


class UnitConversion:
    """Contains class methods that will convert a value of a certain unit to
    another type of unit. All methods have the same arguement.
    Arguments:
        * value [int/float]: the value to convert
        * initialUnit [str]: the the units of the value
        * newUnit [str]: the unit to convert the value to.
        * maxPrecision=4 [int]: Python can produce a floating point error
          working with decimals. After the conversion, the value will be
          rounded to the number defined as maxPrecision.
    """

    @classmethod
    def convert_temperature(cls, value, initialUnit, newUnit, maxPrecision=10):
        """Converts temperatures to new units."""
        if initialUnit == 'kelvin' and newUnit == 'celsius':
            # Python
            return round(value - 273.15, maxPrecision)

        raise ValueError(
            f'temperature convert of {initialUnit} to {newUnit} is not supported.'
        )

if __name__ == "__main__":
    print(
        UnitConversion.convert_temperature(99, 'kelvin', 'celsius')
    )