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


class TestResponseBuilder(unittest.TestCase):
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
