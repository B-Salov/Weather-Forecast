"""WEATHER FORECAST
This program get current weather and write it in a storage.
If the data is more than one day old, then it is overwritten.

  --Project Plan--
* Weather forecast for a couple of days
* Create output style
"""
import json
import requests
from pprint import pprint
from datetime import datetime


class OpenWeatherForecast:

    def __init__(self, city):
        self.city = city

    def create_request(self):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}' \
              '&units=metric&appid=9f886e7aea62aa740e5aa61a638a572d'

        current_weather = requests.get(url).json()
        weather_data = current_weather['main']

        return weather_data


class CacheData:

    def __init__(self, city, storage):
        self.city = city
        self.storage = storage
        self.get_forecast = OpenWeatherForecast(self.city)

    def get_cache(self):
        data = CacheData.load_data(self)

        if data:
            new_data = self.get_forecast.create_request()
            res = {self.city: new_data, 'time': str(datetime.now())}
            
            city_exist = [i for i in data if self.city in i]

            if city_exist:
                if self.check_time(city_exist[0]['time']):
                    return city_exist[0]
                else:
                    result = []
                    for row in data:
                        if self.city in row:
                            result.append(res)
                            continue

                        result.append(row)

                    CacheData.write_data(self, result)

            else:
                data.append(res)
                CacheData.write_data(self, data)

            return res

    def write_data(self, data):
        with open(self.storage, 'w') as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        try:
            data = json.load(open(self.storage))
        except json.decoder.JSONDecodeError:
            data = None
        except FileNotFoundError:
            data = None

        return data

    @staticmethod
    def check_time(time):
        creation_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        delta_time = datetime.now() - creation_time

        return True if delta_time.days == 0 else False


class CityInfo:

    def __init__(self, city, storage):
        self.city = city
        self._get_weather = OpenWeatherForecast(city)
        self._cache_data = CacheData(city, storage)

    def get_forecast(self):
        weather = self._cache_data.get_cache()

        if not weather:
            new_data = self._get_weather.create_request()
            first_record = [{self.city: new_data, 'time': str(datetime.now())}]

            self._cache_data.write_data(first_record)

            return new_data

        return weather


def _main():
    city = input('Your city --> ')
    storage = 'storage.json'

    city_info = CityInfo(city, storage)
    weather = city_info.get_forecast()

    pprint(weather)


if __name__ == '__main__':
    _main()
