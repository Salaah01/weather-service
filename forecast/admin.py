"""Set up for the admin page allowing interaction with the database objects
directly via the admin page.
"""

# IMPORTS
# Python Core Library

# Third Party Imports
from django.contrib import admin

# Local Imports
from .models import Cities, Forecast


class CitiesAdmin(admin.ModelAdmin):
    """Configures the interation and objects available on the admin page
    for models.Cities (forecast_cities)
    """
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


class ForecastAdmin(admin.ModelAdmin):
    """Configures the interation and objects available on the admin page
    for models.Forecast (forecast_forecast)
    """
    list_display = ('id', 'city', 'temperature', 'humidity', 'pressure',
                    'forecast_for')
    list_display_links = ('id', 'city')
    search_fields = ('id', 'city', 'forecast_for')


# Registering models to the admin page
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Forecast, ForecastAdmin)
