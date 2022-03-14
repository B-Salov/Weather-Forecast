"""WEATHER FORECAST
This program get current weather

  --Project Plan--
* Create a data storage
* Weather forecast for a couple of days
* Create output style
"""


import requests
from pprint import pprint


class OpenWeatherForecast:

    def __init__(self, city):
        self.city = city

    def get_weather(self):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}' \
              '&units=metric&appid=9f886e7aea62aa740e5aa61a638a572d'

        current_weather = requests.get(url).json()
        weather_data = current_weather['main']

        return weather_data


class CityInfo:

    def __init__(self, city):
        self.city = city
        self._current_weather = OpenWeatherForecast(city)

    def get_forecast(self):
        return self._current_weather.get_weather()


def _main():
    city_info = CityInfo('Kiev')
    weather = city_info.get_forecast()

    pprint(weather)


if __name__ == '__main__':
    _main()
