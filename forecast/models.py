"""Creates and maintains the database tables (models).
The module will handle the following models:
    * Cities: contains a list of cities.
    * Forecast: Contains weather forecasts for cities at various times.
"""

# IMPORTS
# Python Core Imports

# Third Party Imports
from django.db import models

# Local Imports


class Cities(models.Model):
    """Contains a list of all the cities around the world.
    PRIMARY KEY: name
    FOREIGN KEYS: None
    """
    name = models.CharField(max_length=50, primary_key=True, unique=True)

    class Meta:
        verbose_name_plural = "Cities"


class Forecast(models.Model):
    """Contains weather forecasts at different times for cities around the
    world.
    This
    PRIMARY KEY: id
    FOREIGN KEYS: - city: models.Cities
    """
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    humidity = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    # forecast_for contains date and time for the forcast.
    # This could be a models.DateTimeField but not all databases can support
    # this field type.
    # To provide compatibility between all databases, this is an integer
    # field where the value will be in the format YYYYMMDDHHMM (time will be
    # stored as 24hr format.)
    forecast_for = models.BigIntegerField()
