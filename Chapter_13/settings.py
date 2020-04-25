"""Python Cookbook

Chapter 13, recipe 4, Using class-as-namespace for configuration values.
Settings.
"""


class Configuration:
    """
    Generic Configuration
    """

    url = {"scheme": "http", "netloc": "forecast.weather.gov", "path": "/shmrn.php"}


class Bahamas(Configuration):
    """
    Weather forecast for Offshore including the Bahamas
    """

    query = {"mz": ["AMZ117", "AMZ080"]}


class Chesapeake(Configuration):
    """
    Weather for Chesapeake Bay
    """

    query = {"mz": ["ANZ532"]}
