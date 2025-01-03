#!/usr/bin/env python3
import datetime
import pytz
import requests
import json
import pandas as pd

# TODO add UV index, add cloudcover (low*0.7 + mid * 0.3) for p cloudy, add night vs day for sun/clear night and pcloudy day/pcloudy night, 
# add heavy rain, add windy, 

class Weather():
    def __init__(self) -> None:
        self.weather_dict = self.update_weather()
        pd.set_option('display.max_columns', 500)
        # print(json.dumps(weather_dict, indent=4))

    def update_weather(self) -> dict:
        response = requests.get((
        'https://api.open-meteo.com/v1/forecast?latitude=38.8951&longitude=-77.0364'
        '&hourly=uv_index,is_day,cloudcover_low,cloudcover_mid,'
        'apparent_temperature,precipitation_probability,precipitation,snowfall,'
        'cloudcover,visibility,windspeed_10m,windgusts_10m&temperature_unit=fahrenheit'
        '&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York&current=temperature_2m,apparent_temperature&forecast_days=1'
        )).json()

        return response


# dict_keys(['time', 'uv_index', 'is_day', 'cloudcover_low', 'cloudcover_mid', 
#            'apparent_temperature', 'precipitation_probability', 'precipitation', 
#            'snowfall', 'cloudcover', 'visibility', 'windspeed_10m', 'windgusts_10m'])
    def get_weather_dict_hourly(self) -> dict:

        hourly = self.weather_dict.get('hourly').copy()
        for k in hourly.keys():
            hourly.update({k:hourly.get(k)[:23]})

        return hourly
    
    

    def print_weather_dict(self):
        print(json.dumps(self.weather_dict, indent=2))



    def is_rain_above_percent(self, percent: int) -> bool:
        rain_probabilities_list = self.get_weather_dict_hourly().get('precipitation_probability')
        return (max(rain_probabilities_list) >= percent)
    


    def get_daily_apparent_temp_extrema(self) -> dict:
        high = round(max(self.get_weather_dict_hourly().get('apparent_temperature')))
        low = round(min(self.get_weather_dict_hourly().get('apparent_temperature')))
        return {'high' : high, 'low' : low}
    


    def get_cloud_cover(self):
        cloudcover_low_list = self.get_weather_dict_hourly().get('cloudcover_low')
        cloudcover_mid_list = self.get_weather_dict_hourly().get('cloudcover_mid')
        cloudcover_low_avg = sum(cloudcover_low_list)/len(cloudcover_low_list)
        cloudcover_mid_avg = sum(cloudcover_mid_list)/len(cloudcover_mid_list)
        return cloudcover_low_avg * 0.7 + cloudcover_mid_avg * 0.3
    


    def is_foggy(self) -> bool:
        return min(self.get_weather_dict_hourly().get('visibility')) < 1000
    


    def is_snowing(self) -> bool:
        return max(self.get_weather_dict_hourly().get('snowfall')) > 0.25



    def uv_index_list(self) -> list:
        return self.get_weather_dict_hourly().get('uv_index')
    


    def get_current_temperature(self) -> float:
        return self.weather_dict.get('current').get('apparent_temperature')

    
    def get_current_windspeed_mph(self) -> float:
        current_hour = datetime.datetime.now(pytz.timezone('US/Eastern')).hour
        return self.get_weather_dict_hourly().get('windspeed_10m')[current_hour]
    
    def get_total_rain(self) -> float:
        return sum(self.get_weather_dict_hourly().get('precipitation'))
        



if __name__ == "__main__":
    weather_instance = Weather()
    # print(weather_instance.uv_index_list())
    # print(weather_instance.get_weather_dict_hourly().get('time'))
    # print(datetime.datetime.now(pytz.timezone('US/Eastern')).hour)
    weather_instance.print_weather_dict()
    weather_instance.get_current_temperature()
    # print(weather_instance.get_weather_dict_hourly())
    # print(weather_instance.get_total_rain())
            
