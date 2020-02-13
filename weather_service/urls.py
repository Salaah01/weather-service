"""weatherservice Root URL Configuration
Will act as the main hub for routing urls to different apps which will handle
the url accordingly.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forecast.urls'))
]
