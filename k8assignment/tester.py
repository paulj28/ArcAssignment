import json
import requests

actual_data={'myFavouriteAthlete': 'Lionel Messi'}

def validate():
    base_req='http://localhost:8000/'
    x=requests.get(base_req)
    if(x.json()==actual_data):
        print(True)
    else:
        print(False)

validate()