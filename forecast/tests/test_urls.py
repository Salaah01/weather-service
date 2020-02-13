"""Unittests for the own_api.urls.
Tests will check that the the urls resolve the correct view.
"""


# IMPORTS
# Python Core Library

# Third Party Imports
from django.test import SimpleTestCase
from django.urls import reverse, resolve

# Local Imports
from ..views import ping, forecast


class TestUrls(SimpleTestCase):
    """Unittest to check that the urls resolve the correct view."""

    def test_ping(self):
        """Test that the "ping" url resolves views.ping."""
        url = reverse('ping')
        self.assertEquals(resolve(url).func, ping)

    def test_forecast_valid(self):
        """Test that the "forecast" url resolves views.forecast."""
        url = reverse('forecast', args=['london'])
        self.assertEquals(resolve(url).func, forecast)
