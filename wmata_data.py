#!/usr/bin/env python3
import requests
import json
import header
import pandas as pd

# class WmataData():
#     def __init__(self) -> None:
        # self.train_dict = self.update_train_status()
        # print(json.dumps(weather_dict, indent=4))

    # def update_weather(self) -> dict:
    #     response = requests.get((
    #     'https://api.open-meteo.com/v1/forecast?latitude=38.8951&longitude=-77.0364'
    #     '&hourly=apparent_temperature,precipitation_probability,precipitation'
    #     '&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
    #     '&forecast_days=1'
    #     )).json()
    #     # print(json.dumps(response, indent=4))
    #     return response

    # def get_weather_dict(self):
    #     return self.weather_dict

    # def is_rain_above_percent(self, percent) -> bool:
    #     rain_probabilities_list = self.weather_dict.get('hourly').get('precipitation_probability')
    #     return (max(rain_probabilities_list) >= percent)
    
    # # TODO combine into one function
    # def get_daily_high_apparent_temp(self):
    #     return round(max(self.weather_dict.get('hourly').get('apparent_temperature')))
    
    # def get_daily_low_apparent_temp(self):
    #     return round(min(self.weather_dict.get('hourly').get('apparent_temperature')))
    
    # def print_weather_dict(self):
    #     df = pd.DataFrame.from_dict(self.weather_dict.get('hourly'))
    #     print(df)
            



# def json_print(response_json):
#     print(json.dumps(response_json, indent=4))

# parameters={'LineCode':'GR'}
# response = requests.get("https://api.wmata.com/Rail.svc/json/jStations?", headers=header.apiKey, params=parameters)
# response = response.json()
# # print(json.dumps(response, indent=4))

# # json_print(response.get('Stations'))

# station_names = []
# for s in response.get('Stations'):
#     station_names.append(s.get('Name'))

# print(station_names)


silver = ['Ashburn', 'Loudoun Gateway', 'Washington Dulles International Airport', 'Innovation Center',
'Herndon', 'Reston Town Center', 'Wiehle-Reston East', 'Spring Hill', 'Greensboro', 'Tysons', 'McLean',
'East Falls Church', 'Ballston-MU', 'Virginia Square-GMU', 'Clarendon', 'Court House', 'Rosslyn',
'Foggy Bottom-GWU', 'Farragut West', 'McPherson Square', 'Metro Center', 'Federal Triangle',
'Smithsonian', "L'Enfant Plaza", 'Federal Center SW', 'Capitol South', 'Eastern Market', 'Potomac Ave',
'Stadium-Armory', 'Benning Road', 'Capitol Heights', 'Addison Road-Seat Pleasant', 'Morgan Boulevard',
'Downtown Largo']

blue = ['Franconia-Springfield', 'Van Dorn Street', 'King St-Old Town', 'Braddock Road', 'Potomac Yard',
'Ronald Reagan Washington National Airport', 'Crystal City', 'Pentagon City', 'Pentagon', 
'Arlington Cemetery', 'Rosslyn', 'Foggy Bottom-GWU', 'Farragut West','McPherson Square', 'Metro Center', 
'Federal Triangle', 'Smithsonian', "L'Enfant Plaza", 'Federal Center SW', 'Capitol South', 'Eastern Market',
'Potomac Ave','Stadium-Armory', 'Benning Road', 'Capitol Heights', 'Addison Road-Seat Pleasant', 
'Morgan Boulevard', 'Downtown Largo']

orange = ['Vienna/Fairfax-GMU', 'Dunn Loring-Merrifield', 'West Falls Church', 'East Falls Church',
'Ballston-MU', 'Virginia Square-GMU', 'Clarendon', 'Court House', 'Rosslyn', 'Foggy Bottom-GWU',
'Farragut West', 'McPherson Square', 'Metro Center', 'Federal Triangle', 'Smithsonian', 
"L'Enfant Plaza", 'Federal Center SW', 'Capitol South', 'Eastern Market', 'Potomac Ave',
'Stadium-Armory', 'Minnesota Ave', 'Deanwood', 'Cheverly', 'Landover', 'New Carrollton']

red = ['Shady Grove', 'Rockville', 'Twinbrook', 'North Bethesda', 'Grosvenor-Strathmore',
'Medical Center', 'Bethesda', 'Friendship Heights', 'Tenleytown-AU', 'Van Ness-UDC', 'Cleveland Park',
'Woodley Park-Zoo/Adams Morgan', 'Dupont Circle', 'Farragut North', 'Metro Center', 'Gallery Pl-Chinatown',
'Judiciary Square', 'Union Station', 'NoMa-Gallaudet U', 'Rhode Island Ave-Brentwood', 'Brookland-CUA', 
'Fort Totten', 'Takoma', 'Silver Spring', 'Forest Glen', 'Wheaton', 'Glenmont']

yellow = ['Huntington', 'Eisenhower Avenue', 'King St-Old Town', 'Braddock Road', 'Potomac Yard',
'Ronald Reagan Washington National Airport', 'Crystal City', 'Pentagon City', 'Pentagon',
"L'Enfant Plaza", 'Archives-Navy Memorial-Penn Quarter', 'Gallery Pl-Chinatown', 
'Mt Vernon Sq 7th St-Convention Center', 'Shaw-Howard U', 'U Street/African-Amer Civil War Memorial/Cardozo',
'Columbia Heights', 'Georgia Ave-Petworth', 'Fort Totten', 'West Hyattsville', 'Hyattsville Crossing',
'College Park-U of Md', 'Greenbelt']

green = ['Branch Ave', 'Suitland', 'Naylor Road', 'Southern Avenue', 'Congress Heights', 'Anacostia',
'Navy Yard-Ballpark', 'Waterfront', "L'Enfant Plaza", 'Archives-Navy Memorial-Penn Quarter',
'Gallery Pl-Chinatown', 'Mt Vernon Sq 7th St-Convention Center', 'Shaw-Howard U', 
'U Street/African-Amer Civil War Memorial/Cardozo', 'Columbia Heights', 'Georgia Ave-Petworth',
'Fort Totten', 'West Hyattsville', 'Hyattsville Crossing', 'College Park-U of Md', 'Greenbelt']