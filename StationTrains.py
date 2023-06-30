import requests
import json
import header

class StationTrains:

    #response = requests.get("https://api.wmata.com/Misc/Validate?", headers=header.apiKey)
    #print(response.json())


    # parameters={'LineCode':'SV'}
    # response = requests.get("https://api.wmata.com/Rail.svc/json/jStations?", headers=header.apiKey, params=parameters)
    # print(json.dumps(response.json(), indent=4))


    # parameters={'StationCodes':'D07'}
    response = requests.get("https://api.wmata.com/StationPrediction.svc/json/GetPrediction/C02", headers=header.apiKey)
    trainList = response.json().get("Trains")
    for t in trainList:
        print(t.get("Line"), " ", t.get("Min"))

    # print(json.dumps(response.json(), indent=4))

    # response = requests.get("https://api.wmata.com/TrainPositions/StandardRoutes?contentType=json", headers=header.apiKey)
    # print(json.dumps(response.json(), indent=4))


