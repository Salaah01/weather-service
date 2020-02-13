"""Unittests for the models.
Will perform the following tests:
    * Check that all cities are in models.Cities.
    * Test entry onto models.Forcast
"""


# IMPORTS
# Python Core Library
from datetime import datetime

# Third Party Imports
from django.test import TestCase

# Local Imports
import corefunctions
from ..models import Cities, Forecast


class TestCities(TestCase):
    """An empty class to begin with, test_generator will be used to
    iteratively add tests onto the class.
    """


def test_cities_test_generator():
    """Generates tests to be attached to TestCities.
    The test will check that all cities have a record on the database.
    The initial input of all cities onto the database is handled by
    migration 2.
    """

    def base_test(testPassed, failMessage=None):
        def test(self):
            self.assertTrue(testPassed, failMessage)
        return test

    setattr(TestCities, 'test_1', base_test(1, 1))

    for city in corefunctions.all_cities:
        # By using .get, either the record or None will be returned.
        querySet = Cities.objects.get(name=city)
        testString = f'test_{city}'

        # By using .get when creating querySet, the test in essence has
        # already been done as it'll either return the record or None.
        if querySet:
            setattr(TestCities, testString, base_test(True))
        else:
            failMessage = f'{city} not found in the database'
            setattr(test_cities_test_generator, testString,
                    base_test(False, failMessage))


test_cities_test_generator()


class TestForecast(TestCase):
    """Test to ensure that the models.Forecast stores data correctly."""

    def test_valid_entry(self):

        testData = {
            'city': 'london',
            'humidity': 1.44,
            'pressure': 1.22,
            'temperature': 5.2
        }

        newEntry = Forecast.objects.create(
            city=Cities.objects.get(name=testData['city']),
            humidity=testData['humidity'],
            pressure=testData['pressure'],
            temperature=testData['temperature'],
            forecast_for=corefunctions.date_to_int(datetime.today())
        )
        newEntry.save()
        dbItem = Forecast.objects.get(
            city=testData['city'],
            humidity=testData['humidity'],
            pressure=testData['pressure'],
            temperature=testData['temperature'],
        )

        if dbItem:
            self.assertEquals(testData['city'], dbItem.city.name)
            self.assertEquals(testData['humidity'], dbItem.humidity)
            self.assertEquals(testData['pressure'], dbItem.pressure)
            self.assertEquals(testData['temperature'], dbItem.temperature)
        else:
            self.assertTrue(False, 'Test item could not be found.')
