"""Unittests for the own_api.views.
Tests will check that the the views render correctly.
The following views will be tested:
    * views.ping
    * views.forecast
"""

# IMPORTS
# Python Core Library
import os
import json

# Third Party Imports
from django.test import Client, SimpleTestCase
from django.urls import reverse

# Local Imports


class TestPing(SimpleTestCase):
    """Unittest to check that the urls resolve the correct view. when pinging
    the server (/ping).
    """

    def setUp(self):
        client = Client()
        self.response = client.get(reverse('ping'))

    def test_ping_loads(self):
        """Test that the ping view loads."""

        self.assertEquals(self.response.status_code, 200)

    def test_ping_content(self):
        """Test that the ping view's content is correct."""
        with open(os.path.join(os.getcwd(), 'VERSION'), 'r') as f:
            version = f.read()

        content = json.loads(self.response.content)
        self.assertEquals(content['name'], 'weatherservice')
        self.assertEquals(content['status'], 'ok')
        self.assertEquals(content['version'], version)


class TestForcast(SimpleTestCase):
    """Unittest to check that the urls resolve the correct view. when
    retrieving the forecast for a city.
    Tests will check the following:
        * 404 response returned when provided incorrect city.
    """

    def setUp(self):
        """Sets up for each test"""
        self.client = Client()

    def test_invalid_city(self):
        """Test that an invalid city would return a 404 with an error message
        in the content.
        """
        response = self.client.get(reverse('forecast', args=['westeros']))
        content = json.loads(response.content)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(content['error'], "Cannot find city 'westeros'")
        self.assertEquals(content['error_code'], 'city not found')
