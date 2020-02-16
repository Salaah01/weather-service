"""Configurations for the forecast app".
This module should not do any calculations but instead act as a central hub
for containing certain variables which will be referenced throughout the
forecast app.

Any variables which may change and/or is referenced by multiple modules should
be referenced here so that any future updates can be done in the config thus
preventing having to search for variables throughout all the modules.
"""

# Imports
# Python Core Imports
import os
from datetime import datetime

# Third Party Imports

# Local Imports

# Open Weather Map URL
API_BASE_URL = f"http://api.openweathermap.org/data/2.5/forecast?appid={os.getenv('OWM_API')}&q="

# Maximum number of days into the future a forecast can be retrieved.
MAX_FORCAST_DAYS = 5

# The time interval between any two sets of datapoints.
API_TIME_INTERVAL_MINS = 180
