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

# Third Party Imports

# Local Imports

# Open Weather Map API Key
OWN_API = os.getenv('OWN_API')