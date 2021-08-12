"""Constants for integration_blueprint."""
# Base component constants
NAME = "DSNY"
DOMAIN = "dsny"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ISSUE_URL = "https://github.com/tjhorner/home-assistant-dsny/issues"

# Platforms
BINARY_SENSOR = "binary_sensor"
PLATFORMS = [BINARY_SENSOR]


# Configuration and options
CONF_HOUSE_NUMBER = "house_number"
CONF_STREET_NAME = "street_name"
CONF_BOROUGH = "borough"
VALID_BOROUGHS = ["Brooklyn", "Manhattan", "Queens", "Bronx", "Staten Island"]

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
