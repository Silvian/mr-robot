import os
import requests

from errbot import BotPlugin, botcmd


class Weather(BotPlugin):
    """Weather reports from any specified city location."""

    WEATHER_API = "http://api.weatherstack.com/current"
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", None)

    @botcmd
    def get_weather(self, msg, args):
        """Retrieve weather data from any specified city location."""
        if not args:
            return "Please specify a city name."
        return self.get_weather_api(args)

    def get_weather_api(self, city_name):
        """Perform weather api request."""
        if not self.WEATHER_API_KEY:
            raise Exception("No weather api key configured. :persevere:")

        query_string = {
            "query": city_name,
            "access_key": self.WEATHER_API_KEY,
        }

        response = requests.get(
            url=self.WEATHER_API,
            params=query_string,
        )
        if response.status_code != 200:
            raise Exception("Weather exception: {}".format(response.text))

        response_data = response.json()
        if response_data.get("success", None):
            if not response_data["success"]:
                raise Exception("Weather exception: {}".format(response_data["error"]["info"]))

        location_name = response_data["location"]["name"]
        country = response_data["location"]["country"]
        description = response_data["current"]["weather_descriptions"][0]
        temp = response_data["current"]["temperature"]

        weather_response = "The weather in {location_name}, {country} is {description}, with a temperature {temp} deg ".format(
            location_name=location_name,
            country=country,
            description=description,
            temp=temp,
        )
        return weather_response
