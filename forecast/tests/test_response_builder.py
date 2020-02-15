"""Unittst for the response_builder module.
Will test the following:
    * Returns a 404 response with some content when an incorrect city is
      passed into the url. e.g: /forecast/westeros
"""

# IMPORTS
# Python Core Library
import unittest
import json
from types import SimpleNamespace

# Third Party Imports
from django.test import Client, TestCase
from django.urls import reverse
from django.http import HttpResponse


# Local Imports
from ..response_builder import ResponseBuilder
from ..models import Forecast


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

    def test_API_called_once_only(self):
        """Test that the API is called once only when querying for a
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
