"""Renders forecast related views. These views include:
    * /ping: pings the service (JSON response)
    */forecast/<city>: Gives weather information on a city.
"""


# IMPORTS
# Python Core Imports
import os
import json

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


def forecast(request, city):
    """Returns weather information on city."""
    return ResponseBuilder(request, city).get_response()
