#!/usr/bin/env python3
from datetime import datetime, timedelta, date
import pytz
import requests
import json
import pandas as pd
import pickle

# TODO add UV index, add cloudcover (low*0.7 + mid * 0.3) for p cloudy, add night vs day for sun/clear night and pcloudy day/pcloudy night, 
# add heavy rain, add windy, 

class Weather():
    def __init__(self) -> None:
        self.weather_dict = self.update_weather()
        # print(json.dumps(weather_dict, indent=4))

    def update_weather(self) -> dict:
        # response = requests.get((
        # 'https://api.open-meteo.com/v1/forecast?latitude=38.8951&longitude=-77.0364'
        # '&hourly=uv_index,is_day,cloudcover_low,cloudcover_mid,'
        # 'apparent_temperature,precipitation_probability,precipitation,snowfall,'
        # 'cloudcover,visibility,windspeed_10m,windgusts_10m&temperature_unit=fahrenheit'
        # '&windspeed_unit=mph&precipitation_unit=inch&forecast_days=2'
        # )).json()
        # # print(json.dumps(response, indent=4))

        file = open('weather_dict_temp', 'rb')
        response = pickle.load(file)
        file.close()

        return response


# dict_keys(['time', 'uv_index', 'is_day', 'cloudcover_low', 'cloudcover_mid', 
#            'apparent_temperature', 'precipitation_probability', 'precipitation', 
#            'snowfall', 'cloudcover', 'visibility', 'windspeed_10m', 'windgusts_10m'])
    def get_weather_dict(self, day=-1) -> dict:
        if day == -1:
            return self.weather_dict
        elif day == 0:
            return weather_instance.get_weather_dict().get('hourly')[:23]
        elif day == 1:
            return weather_instance.get_weather_dict().get('hourly')[24:]
    
    def print_weather_dict(self):
        df = pd.DataFrame.from_dict(self.weather_dict.get('hourly'))
        print(df)

    def is_rain_above_percent(self, percent: int) -> bool:
        current_time = datetime.now(pytz.timezone('US/Eastern'))
        hour = current_time.hour

        rain_probabilities_list = self.weather_dict.get('hourly').get('precipitation_probability')
        
        # return max of current hour onwards - useful when it rains early in the morning but not afterwards
        return (max(rain_probabilities_list[hour:]) >= percent)
    

    def get_daily_apparent_temp_extrema(self):
        high = round(max(self.weather_dict.get('hourly').get('apparent_temperature')))
        low = round(min(self.weather_dict.get('hourly').get('apparent_temperature')))
        return {'high' : high, 'low' : low}
    

    def get_cloud_cover(self):
        current_time = datetime.now(pytz.timezone('US/Eastern'))
        hour = current_time.hour

        # cloudcover from current hour onwards
        cloudcover_low_list = self.weather_dict.get('hourly').get('cloudcover_low')[hour:]
        cloudcover_mid_list = self.weather_dict.get('hourly').get('cloudcover_mid')[hour:]
        cloudcover_low_avg = sum(cloudcover_low_list)/len(cloudcover_low_list)
        cloudcover_mid_avg = sum(cloudcover_mid_list)/len(cloudcover_mid_list)
        return cloudcover_low_avg * 0.7 + cloudcover_mid_avg * 0.3
    

    def is_foggy(self) -> bool:
        return min(self.weather_dict.get('hourly').get('visibility')) < 1000
    
    def is_snowing(self) -> bool:
        return max(self.weather_dict.get('hourly').get('snowfall')) > 0.25


if __name__ == "__main__":
    weather_instance = Weather()
    weather_instance.get_cloud_cover()
    weather_instance.print_weather_dict()
    weather_instance.weather_dict = {}

    # now = datetime.now(pytz.timezone('US/Eastern'))

    # if now.hour < 18:
    #     weather_instance.get_weather_dict().get('hourly')[:18]
    # else:
    #     weather_instance.get_weather_dict().get('hourly')[18:18]

#     row_time = pytz.timezone('US/Eastern').localize(dateutil.parser.parse(weather_instance.get_weather_dict().get('hourly').get('time')[26]))
#     # now_local = datetime.now(pytz.timezone('US/Eastern'))
#     today_at_6 = pytz.timezone('US/Eastern').localize(datetime.combine(datetime.now(pytz.timezone('US/Eastern')).date(), datetime.min.time()) + timedelta(hours=18))
#     diffretiation = today_at_6 - row_time
    
    
# # insertion_date = dateutil.parser.parse('2018-03-13T17:22:20.065Z')
# # diffretiation = pytz.utc.localize(datetime.datetime.utcnow()) - insertion_date

#     print(today_at_6)
#     print(row_time)
#     print(diffretiation)

# if diffretiation.days>30:
#     print "The insertion date is older than 30 days"

# else:
#     print "The insertion date is not older than 30 days"
# #The insertion date is older than 30 days
            