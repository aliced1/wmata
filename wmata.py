#!/usr/bin/env python3
import requests
import json
import header
import pandas as pd

        # Train format: {'Car': '8', 'Destination': 'Largo', 'DestinationCode': 'G05', 'DestinationName': 'Downtown Largo',
        #  'Group': '1', 'Line': 'BL', 'LocationCode': 'C02', 'LocationName': 'McPherson Square', 'Min': 'BRD'}

        # Line codes are RD - Red    YL - Yellow    GR - Green    BL - Blue    OR - Orange    SV - Silver

class Wmata():
    def __init__(self) -> None:
        pd.set_option('display.max_columns', 500)
        self.init_stations_all_lines()

    def json_print(self, response_json):
        print(json.dumps(response_json, indent=4))

    def get_trains_for_station(self, station: str) -> dict:
        """Check the incoming trains for a station

        Keyword arguments:
        station -- The WMATA station code as a str (e.g. 'C02')
        """
        # TODO check input

        request_string = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/' + station

        response = requests.get(request_string, headers=header.apiKey)
        return response.json().get("Trains")
   

    # line should be linecode, e.g. 'SV'
    def get_closest_train(self, station: str, line: str, direction: str) -> str:
        trainList = self.get_trains_for_station(station)

        for t in trainList:
            if t.get('Line') != line: continue
            
            t_direction = self.calculate_train_direction(t.get('DestinationName'), t.get('Line'))



            if t_direction != direction: continue

            return t.get('Min')
            # print(t.get('Line'), ' ', t.get('Min'), ' ', t.get('DestinationName'), ' ', direction)
            # if t.get('Line') == 'SV':


    # 0 indicates west/south along the line relative to the center, 1 indicates east/north
    def calculate_train_direction(self, stationName: str, line: str) -> str:
        line = self.line_code_mappings.get(line) 
        destination_index = line.get(stationName)

        if destination_index is None:
            return None

        halfway_index = round(len(line)/2)
        difference = halfway_index - destination_index
        if difference < 0: return 'east'
        else: return 'west'

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

        self.line_code_mappings = {'RD':self.red, 'YL':self.yellow, 'GR':self.green, 'BL':self.blue, 'OR':self.orange, 'SV':self.silver}




if __name__ == "__main__":
    wmata_instance = Wmata()
    print(wmata_instance.get_closest_train('D08', 'SV', 'west'))
    wmata_instance.json_print(wmata_instance.get_trains_for_station('D08'))