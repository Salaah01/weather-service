"""Builds the response for the forecast view. The response will be a
JSON HttpRespose.
"""

# IMPORTS
# Python Core Imports
import json

# Third Party Imports
from django.http import HttpResponse

# Local Imports
from . import config
import corefunctions


class ResponseBuilder:
    """Builds the response for the forecast view.
    Arguments:
    request [obj]: HTTP request object
    city [str]: city name
    """

    def __init__(self, request, city):
        # Arguments attached to the self object.
        self.request = request.GET
        self.city = city

        # Will be build dynamically with information regarding any units
        # need to be converted. e.g: for temperature, convert celsius to
        # fahrenheit.
        self.paramaters = {}

        # Build the response
        self._response = self._set_response()

    def _set_response(self):
        """Sets the HTTP response"""
        contentType = 'application/json; charset=utf-8'

        if self.city not in corefunctions.all_cities:
            content = json.dumps({
                "error": f"Cannot find city '{self.city}'",
                "error_code": "city not found"
            })
            return HttpResponse(content, contentType, 404)
        else:
            return HttpResponse("<h1>Forecast Page</h1>")

    def get_response(self):
        """Gets the HTTP response"""
        return self._response
