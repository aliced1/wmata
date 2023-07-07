#!/usr/bin/env python3
import requests
import json

class Weather():
    def __init__(self) -> None:
        self.weather_dict = self.update_weather()
        # print(json.dumps(weather_dict, indent=4))

    def update_weather(self) -> requests.Response:
        response = requests.get((
        'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41'
        '&hourly=apparent_temperature,precipitation_probability,precipitation'
        '&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
        '&forecast_days=1'
        )).json()
        # print(json.dumps(response, indent=4))
        return response

    def get_weather_dict(self):
        return self.weather_dict

    def is_rain_above_percent(self, percent) -> bool:
        rain_probabilities_list = self.weather_dict.get('hourly').get('precipitation_probability')
        return (max(rain_probabilities_list) >= percent)

    def test_print(self):
        print(self.weather_dict.get('hourly').get('precipitation_probability'))
