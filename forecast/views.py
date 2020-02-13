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


def ping(request):
    """Function to ping the server. Returns a response indicating that the
    server is running.
    """
    return HttpResponse("<h1>Ping Page</h1>")


def forecast(request, city):
    """Returns weather information on city."""
    return HttpResponse('<h1>Forecast Page</h1>')
