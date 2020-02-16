"""weatherservice Root URL Configuration
Will act as the main hub for routing urls to different apps which will handle
the url accordingly.
"""

import json

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forecast.urls'))
]

contentType = 'application/json; charset=utf-8'


handler404 = "forecast.views.handler404"
handler500 = "forecast.views.handler500"
