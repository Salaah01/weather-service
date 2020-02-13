"""Routes URLs to views. The following URLs are defined in this module:
    * ping/             Pings the server to check its status
    * forecast/<city>   Routes to a view that will return weather
                        information on city.
"""

# IMPORTS
# Python Core Library

# Third Party Imports
from django.urls import path

# Local Imports
from . import views

urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path('forecast/<str:city>', views.forecast, name='forecast')
]
