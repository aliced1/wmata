#!/usr/bin/env python3
import requests
import json
import header
import pandas as pd

class Wmata():
    def __init__(self) -> None:
        pd.set_option('display.max_columns', 500)
        self.init_stations_all_lines()

    def json_print(self, response_json):
        print(json.dumps(response_json, indent=4))

    def get_trains_for_station(self, station):
        """Check the incoming trains for a station

        Keyword arguments:
        station -- The WMATA station code as a str (e.g. 'C02')
        """

        # TODO check input

        request_string = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/' + station

        response = requests.get(request_string, headers=header.apiKey)
        trainList = response.json().get("Trains")
        
        # Train format: {'Car': '8', 'Destination': 'Largo', 'DestinationCode': 'G05', 'DestinationName': 'Downtown Largo',
        #  'Group': '1', 'Line': 'BL', 'LocationCode': 'C02', 'LocationName': 'McPherson Square', 'Min': 'BRD'}

        # Line codes are RD - Red    YL - Yellow    GR - Green    BL - Blue    OR - Orange    SV - Silver

        for t in trainList:
            print(t.get('Line'), ' ', t.get('Min'), ' ', t.get('DestinationName'))
        # self.json_print(trainList)

        
        
    
    def calculate_train_direction(self, stationName: str):
        pass

    def init_stations_all_lines(self):
        silver_list = ['Ashburn', 'Loudoun Gateway', 'Washington Dulles International Airport', 'Innovation Center',
        'Herndon', 'Reston Town Center', 'Wiehle-Reston East', 'Spring Hill', 'Greensboro', 'Tysons', 'McLean',
        'East Falls Church', 'Ballston-MU', 'Virginia Square-GMU', 'Clarendon', 'Court House', 'Rosslyn',
        'Foggy Bottom-GWU', 'Farragut West', 'McPherson Square', 'Metro Center', 'Federal Triangle',
        'Smithsonian', "L'Enfant Plaza", 'Federal Center SW', 'Capitol South', 'Eastern Market', 'Potomac Ave',
        'Stadium-Armory', 'Benning Road', 'Capitol Heights', 'Addison Road-Seat Pleasant', 'Morgan Boulevard',
        'Downtown Largo']
        blue_list = ['Franconia-Springfield', 'Van Dorn Street', 'King St-Old Town', 'Braddock Road', 'Potomac Yard',
        'Ronald Reagan Washington National Airport', 'Crystal City', 'Pentagon City', 'Pentagon', 
        'Arlington Cemetery', 'Rosslyn', 'Foggy Bottom-GWU', 'Farragut West','McPherson Square', 'Metro Center', 
        'Federal Triangle', 'Smithsonian', "L'Enfant Plaza", 'Federal Center SW', 'Capitol South', 'Eastern Market',
        'Potomac Ave','Stadium-Armory', 'Benning Road', 'Capitol Heights', 'Addison Road-Seat Pleasant', 
        'Morgan Boulevard', 'Downtown Largo']
        orange_list = ['Vienna/Fairfax-GMU', 'Dunn Loring-Merrifield', 'West Falls Church', 'East Falls Church',
        'Ballston-MU', 'Virginia Square-GMU', 'Clarendon', 'Court House', 'Rosslyn', 'Foggy Bottom-GWU',
        'Farragut West', 'McPherson Square', 'Metro Center', 'Federal Triangle', 'Smithsonian', 
        "L'Enfant Plaza", 'Federal Center SW', 'Capitol South', 'Eastern Market', 'Potomac Ave',
        'Stadium-Armory', 'Minnesota Ave', 'Deanwood', 'Cheverly', 'Landover', 'New Carrollton']
        red_list = ['Shady Grove', 'Rockville', 'Twinbrook', 'North Bethesda', 'Grosvenor-Strathmore',
        'Medical Center', 'Bethesda', 'Friendship Heights', 'Tenleytown-AU', 'Van Ness-UDC', 'Cleveland Park',
        'Woodley Park-Zoo/Adams Morgan', 'Dupont Circle', 'Farragut North', 'Metro Center', 'Gallery Pl-Chinatown',
        'Judiciary Square', 'Union Station', 'NoMa-Gallaudet U', 'Rhode Island Ave-Brentwood', 'Brookland-CUA', 
        'Fort Totten', 'Takoma', 'Silver Spring', 'Forest Glen', 'Wheaton', 'Glenmont']
        yellow_list = ['Huntington', 'Eisenhower Avenue', 'King St-Old Town', 'Braddock Road', 'Potomac Yard',
        'Ronald Reagan Washington National Airport', 'Crystal City', 'Pentagon City', 'Pentagon',
        "L'Enfant Plaza", 'Archives-Navy Memorial-Penn Quarter', 'Gallery Pl-Chinatown', 
        'Mt Vernon Sq 7th St-Convention Center', 'Shaw-Howard U', 'U Street/African-Amer Civil War Memorial/Cardozo',
        'Columbia Heights', 'Georgia Ave-Petworth', 'Fort Totten', 'West Hyattsville', 'Hyattsville Crossing',
        'College Park-U of Md', 'Greenbelt']
        green_list = ['Branch Ave', 'Suitland', 'Naylor Road', 'Southern Avenue', 'Congress Heights', 'Anacostia',
        'Navy Yard-Ballpark', 'Waterfront', "L'Enfant Plaza", 'Archives-Navy Memorial-Penn Quarter',
        'Gallery Pl-Chinatown', 'Mt Vernon Sq 7th St-Convention Center', 'Shaw-Howard U', 
        'U Street/African-Amer Civil War Memorial/Cardozo', 'Columbia Heights', 'Georgia Ave-Petworth',
        'Fort Totten', 'West Hyattsville', 'Hyattsville Crossing', 'College Park-U of Md', 'Greenbelt']

        self.silver = {silver_list[i]: i for i in range(0, len(silver_list))}
        self.blue = {blue_list[i]: i for i in range(0, len(blue_list))}
        self.orange = {orange_list[i]: i for i in range(0, len(orange_list))}
        self.red = {red_list[i]: i for i in range(0, len(red_list))}
        self.yellow = {yellow_list[i]: i for i in range(0, len(yellow_list))}
        self.green = {green_list[i]: i for i in range(0, len(green_list))}




if __name__ == "__main__":
    wmata_instance = Wmata()
    wmata_instance.get_trains_for_station('C02')