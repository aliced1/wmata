import requests
import json
import header

lines_and_stations = {}

def json_print(response_json):
    print(json.dumps(response_json, indent=4))

parameters={'LineCode':'SV'}
response = requests.get("https://api.wmata.com/Rail.svc/json/jStations?", headers=header.apiKey, params=parameters)
response = response.json()
# print(json.dumps(response, indent=4))

# json_print(response.get('Stations'))

station_names = []
for s in response.get('Stations'):
    station_names.append(s.get('Name'))

print(station_names)



