"""Renders forecast related views. These views include:
    * /ping: pings the service (JSON response)
    */forecast/<city>: Gives weather information on a city.
"""


# IMPORTS
# Python Core Imports
import os
import json
import re

# Third Party Imports
from django.http import HttpResponse

# Local Imports
from .response_builder import ResponseBuilder

contentType = 'application/json; charset=utf-8'


def ping(request):
    """Function to ping the server. Returns a response indicating that the
    server is running.
    """
    # Application Version
    with open(os.path.join(os.getcwd(), 'VERSION'), 'r') as f:
        version = f.read()

    response = json.dumps(
        {'name': 'weatherservice', 'status': 'ok', 'version': version}
    )

    return HttpResponse(response, content_type=contentType)


def forecast(request, city=None):
    """Returns weather information on city."""
    return ResponseBuilder(request, city).get_response()


def handler404(request, exception):
    """Handles a 404 HTTP response."""
    url = request.build_absolute_uri()
    if re.match('(/forecast/)|(/forecast)$', url):
        return HttpResponse(
            json.dumps({
                "error": "no city provided",
                "error_code": "invalid request"
            }),
            status=404,
            content_type=contentType
        )
    else:
        return HttpResponse(
            json.dumps({
                "error": "page not found",
                "error_code": "page not found"
            }),
            status=404,
            content_type=contentType
        )

def handler500(request):
    """Handles a 404 HTTP response."""
    return HttpResponse(
        json.dumps({
            "error": "Something went wrong",
            "error_code": "internal server error"
        }),
        status=404,
        content_type=contentType
    )