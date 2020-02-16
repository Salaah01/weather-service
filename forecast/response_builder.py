"""Builds the response for the forecast view. The response will be a
JSON HttpRespose.
"""

# IMPORTS
# Python Core Imports
from datetime import datetime, timedelta
import time
import json

# Third Party Imports
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
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

        # If the city is not valid, then return a 404.
        # This can be queried against the database, but there is a finite
        # number of cities and so this avoids a database call by checking
        # a local file.
        if self.city not in corefunctions.all_cities:
            response = {
                "error": f"Cannot find city '{self.city}'",
                "error_code": "city not found"
            }

            return self.format_json_response(response, 404)

        else:
            # Check if there is a date, if so, convert the date before
            # continuing.
            if self.request.get('at'):

                # Try and except to handle an invalid date
                try:
                    forecastDate = corefunctions.UnitConversion(
                        self.request.get('at'),
                        'unknown',
                        'datetime'
                    ).convert_date_string()
                except ValueError:
                    response = {
                        'error': 'Invalid date format, use ISO 8601',
                        'error_code': 'invalid date'
                    }
                    return self.format_json_response(response, 400)

                # If the date is in the past or greater than the latest
                # forecast available, return a 400.
                now = datetime.now()
                minDate = datetime(now.year, now.month, now.day)
                maxDate = now + timedelta(days=config.MAX_FORCAST_DAYS)

                if forecastDate < minDate:
                    response = {
                        'error': 'Date is in the past',
                        'error_code': 'invalid date'
                    }
                    return self.format_json_response(response, 400)

                elif forecastDate > maxDate:
                    response = {
                        'error': f'Only able to forecast up to {config.MAX_FORCAST_DAYS} days',
                        'error_code': 'invalid date'
                    }
                    return self.format_json_response(response, 400)

            else:
                forecastDate = datetime.now()
            self.paramaters['at'] = corefunctions.date_to_int(forecastDate)

            # Retrieve the forecast data
            querySet = self.forecast_data(forecastDate)

            # The querySet may return multiple rows of data contain forcast
            # information at different times of the day.
            # Filter the results and return the data at a single time.
            querySet = self.queryset_filter(
                querySet,
                corefunctions.date_to_int(forecastDate),
                'forecast_for'
            )

            # Convert the querySet to a dictionary
            querySet = self.queryset_to_dict(querySet)

            # Configure units in accordance to the paramaters set in the URL.
            querySet = self.format_units(querySet)

            return querySet

    def forecast_data(self, forecastDate):
        """Given a city (string) and a forecast time (int in the format
        YYYYMMDDHHMM or datetime.datetime), return the forcast for a city at
        the specified time.
        """

        # NOTE: Amend the config file to reflect the time it takes before new data
        # by the API would be provided accordingly.

        if isinstance(forecastDate, int):
            forecastDate = corefunctions.int_to_datetime(forecastDate)

        minDate = corefunctions.date_to_int(
            forecastDate
            - timedelta(minutes=config.API_TIME_INTERVAL_MINS)
        )
        maxTime = corefunctions.date_to_int(
            forecastDate
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

        querySet = Forecast.objects.filter(
            city=self.city,
            forecast_for__gte=minDate,
            forecast_for__lte=maxTime
        ).order_by('-forecast_for')

        return querySet

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
            raise HttpResponseServerError()
        else:
            apiData = json.loads(response.content)['list']
            for data in apiData:
                # Some of the data may need to converted to match that which
                # is defined in the docstring.
                # If a piece of data is not converted, it suggests that the
                # API uses the datatype we want.

                # Convert the forecast time epoch to local time.
                forecastDate = time.strftime(
                    '%Y%m%d%H%M',
                    time.localtime(data['dt'])
                )

                newData = Forecast.objects.create(
                    city_id=city,
                    forecast_for=forecastDate,
                    humidity=data['main']['humidity'],
                    pressure=data['main']['pressure'],
                    clouds=data['clouds']['all'],
                    temperature=data['main']['temp']
                )
                newData.save()

    @staticmethod
    def queryset_filter(querySet, forecastDate, timeField):
        """Given a querySet which contains a timeField, find the row of data
        which is nearest to the forecastDate.
        Arguments:
        querySet: Django query set
        forecastDate: date and time in the formation YYYYMMDDHHMM.
        timeField: a field in the querySet which contains a list of times in
                   the format YYYYMMDDHHMM.
        """

        if len(querySet) == 1:
            return querySet[0]
        else:
            querySet = querySet.order_by('-'+timeField)
            initDiff = abs(getattr(querySet[0], timeField) - forecastDate)

        for dataRow in range(1, len(querySet)):
            querySet[dataRow].forecast_for
            diff = abs(getattr(querySet[dataRow], timeField) - forecastDate)
            if diff < initDiff:
                initDiff = diff

            else:
                return querySet[dataRow - 1]
        else:
            return querySet[len(querySet) - 1]

    @staticmethod
    def queryset_to_dict(querySet):
        """Converts the querySet to a dictionary."""

        fields = ['humidity', 'pressure', 'temperature', 'clouds']

        return {field: getattr(querySet, field) for field in fields}

    def format_units(self, querySet):
        """Checks the paramters defined in the URL for any any units that need
        to be converted amd adds the unit type at the end of each unit.
        """

        # Add the "%" unit symbol to humidity
        querySet['humidity'] = str(querySet['humidity']) + '%'

        # Format temperature units.
        # Temperature is stored as kelvins in the database.
        # As a default, the HTTP response will display temperature as celsius.
        if self.request.get('temp_units'):
            tempUnits = self.request.get('temp_units')

            # Validate the units.
            if tempUnits not in ('K', 'C', 'F'):
                response = {
                    'error': 'Invalid temperature units',
                    'error_code': 'invalid_units'
                }

                return self.format_json_response(response, 400)

            if tempUnits == 'K':
                querySet['temperature'] = str(querySet['temperature']) + 'K'
            else:
                querySet['temperature'] = corefunctions.UnitConversion(
                    querySet['temperature'],
                    'K',
                    tempUnits,
                    showUnits=True
                ).convert_temperature()

        else:
            querySet['temperature'] = corefunctions.UnitConversion(
                querySet['temperature'],
                'K',
                'C',
                showUnits=True
            ).convert_temperature()

        # Format temperature units.
        # Temperature is stored as kelvins in the database.
        if self.request.get('pressure_units'):
            pressureUnits = self.request.get('pressure_units').lower()

            # Validate the units.
            supportedUnits = ['pa', 'bar', 'atm', 'torr', 'psi', 'hpa']
            if pressureUnits not in supportedUnits:
                response = {
                    'error': 'Invalid pressure units',
                    'error_code': 'invalid_units'
                }

                return self.format_json_response(response, 400)

            # hPa is the default unit, so no conversions will take place for
            # hPa.
            if pressureUnits == 'hPa':
                querySet['pressure'] = str(querySet['pressure']) + 'hPa'
            else:
                querySet['pressure'] = corefunctions.UnitConversion(
                    querySet['pressure'],
                    'hPa',
                    pressureUnits,
                    showUnits=True
                ).convert_pressure()

        else:
            querySet['pressure'] = str(querySet['pressure']) + 'hPa'

        # Format Cloud Value
        if querySet['clouds'] <= 10:
            querySet['clouds'] = 'clear sky'
        elif querySet['clouds'] <= 36:
            querySet['clouds'] = 'few clouds'
        elif querySet['clouds'] <= 60:
            querySet['clouds'] = 'scattered clouds'
        elif querySet['clouds'] <= 84:
            querySet['clouds'] = 'broken clouds'
        else:
            querySet['clouds'] = 'overcast'

        return self.format_json_response(querySet, 200)

    @staticmethod
    def format_json_response(response=None, status=200):
        """Using the arguments returns a HTTP response.
        response [dict]: response to be converted to JSON.
        status [int]: HTTP status code.
        """
        contentType = 'application/json; charset=utf-8'

        if response:
            return HttpResponse(
                json.dumps(response),
                status=status,
                content_type=contentType,
            )

        # Handle generic errors
        if status == 500:
            return HttpResponse(
                json.dumps({
                    'error': 'Something went wrong',
                    'error_code': 'internal server error'
                })
            )

    def get_response(self):
        """Gets the HTTP response"""
        return self._response
