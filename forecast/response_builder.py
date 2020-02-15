"""Builds the response for the forecast view. The response will be a
JSON HttpRespose.
"""

# IMPORTS
# Python Core Imports
from datetime import datetime, timedelta
import time
import json

# Third Party Imports
from django.http import HttpResponse, HttpResponseServerError
import requests

# Local Imports
from . import config
import corefunctions
from weather_service.settings import DEBUG
from .models import Forecast


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

        # If the city is not valid, then return a 404.
        # This can be queried against the database, but there is a finite
        # number of cities and so this avoids a database call by checking
        # a local file.
        if self.city not in corefunctions.all_cities:
            content = json.dumps({
                "error": f"Cannot find city '{self.city}'",
                "error_code": "city not found"
            })
            return HttpResponse(content, contentType, 404)
        else:
            # Check if there is a date, if so, convert the date before
            # continuing.
            if self.request.get('at'):
                # TODO: complete this path.
                pass
            else:
                forcastDate = datetime.now()
            self.paramaters['at'] = corefunctions.date_to_int(forcastDate)

            self.forecast_data(datetime.now())

            return HttpResponse("<h1>Forecast Page</h1>")

    def forecast_data(self, forecastTime):
        """Given a city (string) and a forecast time (int in the format
        YYYYMMDDHHMM or datetime.datetime), return the forcast for a city at
        the specified time.
        """

        # NOTE: Amend the config file to reflect the time it takes before new data
        # by the API would be provided accordingly.

        if isinstance(forecastTime, int):
            forecastTime = corefunctions.int_to_datetime(forecastTime)

        minDate = corefunctions.date_to_int(
            forecastTime
            - timedelta(minutes=config.API_TIME_INTERVAL_MINS)
        )
        maxTime = corefunctions.date_to_int(
            forecastTime
            + timedelta(minutes=config.API_TIME_INTERVAL_MINS)
        )

        querySet = Forecast.objects.filter(
            city=self.city,
            forecast_for__gte=minDate,
            forecast_for__lte=maxTime
        ).order_by('-forecast_for')

        # If the data does not exist, then call the API.
        if not querySet:
            self.call_API(self.city)

    @staticmethod
    def call_API(city):
        """Fetches a weather forecast from the API for a given city and
        adds this data onto the database.
        The request content will contain data across a number of days with
        across different point through the day.
        The data will be converted and stored into the database.
        The following detail the data will be stored and their units:
        * city: taken from city arg.
        * temperature: celsius
        * humidity: percentage
        * pressure: hPa
        * clouds: percentage
        * forcast_for: integer in the format YYYYMMDDHHMM
        """
        response = requests.get(config.API_BASE_URL + city)
        # If the response is not 200, then raise a 500 error. This assumes
        # that the API URL defined in the config is correct as is the city
        # name.
        if not response.status_code == 200:
            if DEBUG:
                return HttpResponse(response.content, status=500)
            raise HttpResponseServerError
        else:
            apiData = json.loads(response.content)['list']
            for data in apiData:
                # Some of the data may need to converted to match that which
                # is defined in the docstring.
                # If a piece of data is not converted, it suggests that the
                # API uses the datatype we want.

                # Convert the forecast time epoch to local time.
                forecastTime = time.strftime(
                    '%Y%m%d%H%M',
                    time.localtime(data['dt'])
                )

                # Convert the temperature from Kelvins to Celsius.
                temperature = corefunctions.UnitConversion.convert_temperature(
                    data['main']['temp'],
                    'kelvin',
                    'celsius'
                )

                print(temperature)
                newData = Forecast.objects.create(
                    city_id=city,
                    forecast_for=forecastTime,
                    humidity=data['main']['humidity'],
                    pressure=data['main']['pressure'],
                    clouds=data['clouds']['all'],
                    temperature=temperature
                )
                newData.save()






    def get_response(self):
        """Gets the HTTP response"""
        return self._response
