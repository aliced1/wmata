import requests
import json


header = {'api_key':'b614f68d90a24f849b018c81e543704a'}

#response = requests.get("https://api.wmata.com/Misc/Validate?", headers=header)
#print(response.json())


# parameters={'LineCode':'SV'}
# response = requests.get("https://api.wmata.com/Rail.svc/json/jStations?", headers=header, params=parameters)
# print(json.dumps(response.json(), indent=4))


# parameters={'StationCodes':'D07'}
response = requests.get("https://api.wmata.com/StationPrediction.svc/json/GetPrediction/C02", headers=header)
trainList = response.json().get("Trains")
for t in trainList:
	print(t.get("Line"), " ", t.get("Min"))

# print(json.dumps(response.json(), indent=4))

# response = requests.get("https://api.wmata.com/TrainPositions/StandardRoutes?contentType=json", headers=header)
# print(json.dumps(response.json(), indent=4))




# parameters={'LineCode':'GR'}
# response = requests.get("https://api.wmata.com/Rail.svc/json/jStations?", headers=header.apiKey, params=parameters)
# response = response.json()
# # print(json.dumps(response, indent=4))

# # json_print(response.get('Stations'))

# station_names = []
# for s in response.get('Stations'):
#     station_names.append(s.get('Name'))

# print(station_names)


