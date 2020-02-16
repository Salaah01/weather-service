"""Test cases for test_unit_conversion.UnitConversion.
Used by the test_temperature_generator to build the iteratively
add tests to the main test class.
"""

# IMPORTS
# Python Core Imports

# Third Party Imports

# Local Imports
from corefunctions import UnitConversion

testcases = [
    {
        'actual': UnitConversion(99, 'K', 'C').convert_temperature(),
        'expected': -174.15,
        'failMessage': 'Error in converting kelvins (K) to celsius (C)'
    },
    {
        'actual': UnitConversion(99, 'K', 'C', 2, True).convert_temperature(),
        'expected': '-174.15C',
        'failMessage': 'Error in converting kelvins (K) to celsius (C)'
    },
    {
        'actual': UnitConversion(0, 'C', 'K').convert_temperature(),
        'expected': 273.15,
        'failMessage': 'Error in converting celsius (C) to kelvins (K)'
    },
    {
        'actual': UnitConversion(0, 'C', 'K', 2, True).convert_temperature(),
        'expected': '273.15K',
        'failMessage': 'Error in converting celsius (C) to kelvins (K)'
    },
    {
        'actual': UnitConversion(1, 'K', 'F').convert_temperature(),
        'expected': -457.87,
        'failMessage': 'Error in converting kelvins (K) to fahrenheit (F)'
    },
    {
        'actual': UnitConversion(1, 'K', 'F', 2, True).convert_temperature(),
        'expected': '-457.87F',
        'failMessage': 'Error in converting kelvins (K) to fahrenheit (F)'
    },
    {
        'actual': UnitConversion(1, 'hPa', 'Pa').convert_pressure(),
        'expected': 100,
        'failMessage': 'Error in hectopascals (hPa) to pascals (Pa)'
    },
    {
        'actual': UnitConversion(1, 'hPa', 'Pa', 2, True).convert_pressure(),
        'expected': '100Pa',
        'failMessage': 'Error in hectopascals (hPa) to pascals (Pa)'
    },
    {
        'actual': UnitConversion(10, 'hPa', 'bar').convert_pressure(),
        'expected': 0.01,
        'failMessage': 'Error in hectopascals (hPa) to bar (bar)'
    },
    {
        'actual': UnitConversion(10, 'hPa', 'bar', 2, True).convert_pressure(),
        'expected': '0.01bar',
        'failMessage': 'Error in hectopascals (hPa) to bar (bar)'
    },
    {
        'actual': UnitConversion(10, 'hPa', 'atm', 6).convert_pressure(),
        'expected': 0.009869,
        'failMessage': 'Error in hectopascals (hPa) to standard atmosphere (atm)'
    },
    {
        'actual': UnitConversion(10, 'hPa', 'atm', 6, True).convert_pressure(),
        'expected': '0.009869atm',
        'failMessage': 'Error in hectopascals (hPa) to standard atmosphere (atm)'

    },
    {
        'actual': UnitConversion(1, 'hPa', 'Torr', 2).convert_pressure(),
        'expected': 0.75,
        'failMessage': 'Error in hectopascals (hPa) to standard torr (Torr)'
    },
    {
        'actual': UnitConversion(1, 'hPa', 'Torr', 2, True).convert_pressure(),
        'expected': '0.75Torr',
        'failMessage': 'Error in hectopascals (hPa) to standard torr (Torr)'
    },
    {
        'actual': UnitConversion(1, 'hPa', 'psi', 4).convert_pressure(),
        'expected': 0.0145,
        'failMessage': 'Error in hectopascals (hPa) to standard pound per square inch (psi)'
    },
    {
        'actual': UnitConversion(1, 'hPa', 'psi', 4, True).convert_pressure(),
        'expected': '0.0145psi',
        'failMessage': 'Error in hectopascals (hPa) to standard pound per square inch (psi)'
    }
]
