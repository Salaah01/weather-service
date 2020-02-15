"""Unittest for the response_builder module.
The module includes the following test:
    * test_invalid_city:
        Returns a 404 response with some content when an incorrect city is
        passed into the url. e.g: /forecast/westeros.

    * test_API_called_once_only:
        Check that the API is not called if the data requested already exists
        in the database.

    * test_valid_response:
        Check that the module returns the correct response.

"""

# IMPORTS
# Python Core Library
from datetime import datetime, timedelta
import json
from types import SimpleNamespace

# Third Party Imports
from django.test import Client, TestCase
from django.urls import reverse

# Local Imports
import corefunctions
from .. import config
from ..response_builder import ResponseBuilder
from ..models import Cities, Forecast


class TestResponseBuilder(TestCase):
    #     """Unittests for the ResponseBuilder module"""

    def setUp(self):
        """Sets up for each test"""
        self.client = Client()
        self.request = SimpleNamespace(GET={})

    def test_invalid_city(self):
        """Test that an invalid city would would a 404 with an error message
        in the content.
        """
        response = ResponseBuilder(self.request, 'gondor').get_response()
        expected = {
            'content': {
                "error": f"Cannot find city 'gondor'",
                "error_code": "city not found"
            },
            'status': 404
        }

        self.assertEquals(
            json.loads(response.content)['error'],
            expected['content']['error']
        )
        self.assertEquals(
            json.loads(response.content)['error_code'],
            expected['content']['error_code']
        )
        self.assertEquals(
            response.status_code,
            expected['status']
        )

    def zzztest_API_called_once_only(self):
        """Test for call_API method.
        Test that the API is called once only when querying for
        information. When a valid query is sent, if applicable data exists
        in the database, then that data should be returned. Otherwise, the
        call_API method should be called to call the API and populate the
        database.

        This test will call the module twice with the same query and will
        check that the database has only been updated one.
        """
        ResponseBuilder(self.request, 'london').get_response()
        objectsCall1 = len(Forecast.objects.all())
        ResponseBuilder(self.request, 'london').get_response()
        objectsCall2 = len(Forecast.objects.all())

        self.assertEquals(objectsCall1, objectsCall2)

    def test_queryset_filter(self):
        """Tests for the queryset_filter method.
        Test to ensure that the querySet with the value closest to the
        forecast date is returned using the following tests:
            - Method returns the first querySet item if the number of
              items items in querySet = 1.
            - Method returns a 2nd querySet item if the 2nd item has a date
              closest to the forecast date.
            - Method returns the last querySet item if the last item has the
              forecast which is the closest to the desired forecast date.
        """
        # By setting a high API_TIME_INTERVAL_MINS value, the module
        # will not call the API to fetch new values.
        config.API_TIME_INTERVAL_MINS = 100000

        def new_db_item(fieldValue):
            """Function to create a new row in the Forecast table where each
            field value will equal to fieldValue with the exception of those
            which are hard coded.
            """
            newItem = Forecast.objects.create(
                humidity=fieldValue,
                pressure=fieldValue,
                temperature=fieldValue,
                forecast_for=forecastDate,
                city=Cities.objects.get(pk='london'),
                clouds=fieldValue
            )
            newItem.save()

        # Test that where there is only one item in the querySet list,
        # that item is returned.
        forecastDate = corefunctions.date_to_int(
            datetime.now() -
            timedelta(days=3)
        )
        new_db_item(1)

        response = self.client.get(reverse('forecast', args=['london']))
        responseContent = json.loads(response.content)

        self.assertEquals(
            responseContent['temperature'],
            1,
            "Method did not return first record where len(querySet)=1"
        )

        # Test that where is this 3 items querySet list where the second item
        # is closesest to the desired forecast date, that the second querySet
        # item is returned.
        forecastDate = corefunctions.date_to_int(
            datetime.now() -
            timedelta(days=-2)
        )
        new_db_item(2)

        response = self.client.get(reverse('forecast', args=['london']))
        responseContent = json.loads(response.content)

        self.assertEquals(
            responseContent['temperature'],
            2,
            "Method did not return the 2nd querySet where len(querySet)=3"
        )

        # Test that where there is more than 2 items in the querySet list
        # the last item is returned where the last item is closest to the
        # desired forecast date.

        forecastDate = corefunctions.date_to_int(
            datetime.now() -
            timedelta(days=1)
        )
        new_db_item(2)

        forecastDate = corefunctions.date_to_int(
            datetime.now() -
            timedelta(days=10)
        )

        new_db_item(2)

        response = self.client.get(reverse('forecast', args=['london']))
        responseContent = json.loads(response.content)

        self.assertEquals(
            responseContent['temperature'],
            2,
            "Method did not return the 2nd querySet where len(querySet)=3 \
            where the 2nd item is closest to the desired forecast date."
        )


    def zzztest_valid_response(self):
        """Tests that the response from a query is valid.
        Populate the database with specific data and check that the response
        contains that data.
        """

        expectedResults = {
            'humidity': 1,
            'pressure': 2,
            'temperature': 3,
            'clouds': 4
        }

        newItem = Forecast.objects.create(
            humidity=expectedResults['humidity'],
            pressure=expectedResults['pressure'],
            temperature=expectedResults['temperature'],
            forecast_for=corefunctions.date_to_int(datetime.now()),
            city=Cities.objects.get(name='london'),
            clouds=expectedResults['clouds']
        )

        newItem.save()

        response = self.client.get(reverse('forecast', args=['london']))
        responseContent = json.loads(response.content)

        self.assertEquals(response.status_code, 200)

        for field, value in expectedResults.items():
            self.assertEquals(responseContent[field], value)
