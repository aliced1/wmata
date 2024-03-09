#!/usr/bin/env python3
from datetime import datetime
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
        '&windspeed_unit=mph&precipitation_unit=inch&past_days=1&forecast_days=1'
        )).json()

        # DEBUG - for testing without internet
        # file = open('weather_dict_temp', 'rb')
        # response = pickle.load(file)
        # file.close()

        return response


# dict_keys(['time', 'uv_index', 'is_day', 'cloudcover_low', 'cloudcover_mid', 
#            'apparent_temperature', 'precipitation_probability', 'precipitation', 
#            'snowfall', 'cloudcover', 'visibility', 'windspeed_10m', 'windgusts_10m'])
    def get_weather_dict(self) -> dict:

        # return current day if 5PM or earlier, else return tomorrow
        current_time = datetime.now(pytz.timezone('US/Eastern'))

        hourly = self.weather_dict.get('hourly').copy()
        if current_time.hour <= 17:
            for k in hourly.keys():
                hourly.update({k:hourly.get(k)[:23]})
        
        elif current_time.hour > 17:
            for k in hourly.keys():
                hourly.update({k:hourly.get(k)[24:]})
        
        # df = pd.DataFrame.from_dict(hourly)
        # print()
        # print(df)

        return hourly
    
    def print_weather_dict(self):
        df = pd.DataFrame.from_dict(self.weather_dict.get('hourly'))
        print()
        print(df)

    def is_rain_above_percent(self, percent: int) -> bool:
        rain_probabilities_list = self.get_weather_dict().get('precipitation_probability')
        return (max(rain_probabilities_list) >= percent)
    

    def get_daily_apparent_temp_extrema(self):
        high = round(max(self.get_weather_dict().get('apparent_temperature')))
        low = round(min(self.get_weather_dict().get('apparent_temperature')))
        return {'high' : high, 'low' : low}
    

    def get_cloud_cover(self):
        cloudcover_low_list = self.get_weather_dict().get('cloudcover_low')
        cloudcover_mid_list = self.get_weather_dict().get('cloudcover_mid')
        cloudcover_low_avg = sum(cloudcover_low_list)/len(cloudcover_low_list)
        cloudcover_mid_avg = sum(cloudcover_mid_list)/len(cloudcover_mid_list)
        return cloudcover_low_avg * 0.7 + cloudcover_mid_avg * 0.3
    

    def is_foggy(self) -> bool:
        return min(self.get_weather_dict().get('visibility')) < 1000
    
    def is_snowing(self) -> bool:
        return max(self.get_weather_dict().get('snowfall')) > 0.25

    def uv_index_list(self) -> list:
        return self.get_weather_dict().get('uv_index')


if __name__ == "__main__":
    weather_instance = Weather()
    weather_instance.uv_index_list()
    # weather_instance.print_weather_dict()
            
