"""WEATHER FORECAST
This program get current weather

  --Project Plan--
* Create time limits in storage
* Weather forecast for a couple of days
* Create output style
"""
import json
import requests
from pprint import pprint


class OpenWeatherForecast:

    def __init__(self, city):
        self.city = city

    def create_request(self):
        print("Making http request!")
        url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}' \
              '&units=metric&appid=9f886e7aea62aa740e5aa61a638a572d'

        current_weather = requests.get(url).json()
        weather_data = current_weather['main']

        return weather_data


class CacheData:

    def __init__(self, city):
        self.city = city

    def check_in_storage(self):
        data = CacheData.load_data()
        if data:
            for i in data:
                if self.city in i:
                    return i[self.city]

        return None

    def write_data(self, forecast):
        data = CacheData.load_data()

        if not data:
            data = [{self.city: forecast}]
        else:
            data.append({self.city: forecast})

        with open('storage.json', 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load_data():
        try:
            data = json.load(open('storage.json'))
        except json.decoder.JSONDecodeError:
            return None

        return data


class CityInfo:

    def __init__(self, city):
        self.city = city
        self._get_weather = OpenWeatherForecast(city)
        self._cache_data = CacheData(city)

    def get_forecast(self):
        weather = self._cache_data.check_in_storage()

        if not weather:
            forecast = self._get_weather.create_request()
            self._cache_data.write_data(forecast)

            return forecast

        return weather


def _main():
    city_info = CityInfo('Gamburg')
    weather = city_info.get_forecast()

    pprint(weather)


if __name__ == '__main__':
    _main()
