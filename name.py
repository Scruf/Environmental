import json, os
from datetime import datetime
from requests import get
from geopy.geocoders import Nominatim



def get_darksky_response(url, _date):
    requests =  get(url)
    if requests.status_code == 200:
        data = requests.json()["hourly"]
        date_json = {
            _date:{}
        }

        for timestamp in data["data"]:
            date_json[_date].update({
                timestamp["time"]:{
                    "temperature":timestamp["temperature"],
                    "dewPoint":timestamp["dewPoint"],
                    "humidity":timestamp["humidity"]
                }
            })
        with open("sample.json", "w") as fp:
            json.dump(date_json, fp)

    else:
        print(requests.text)

geolocator = Nominatim(user_agent="specify_your_app_name_here")
key = "689904ed285f890e88c17672dfe9b706"



api_url = lambda key, lat, lon, time: f'https://api.darksky.net/forecast/{key}/{lat},{lon},{time}?units=us'

regions = None
with open('Invalid.json', 'r') as fil:
    regions = json.load(fil)

locationArr = []
for country in regions:
    # print(country.keys())
    if country["Region"]:
        for region in country["Region"]:
            geocode = geolocator.geocode(region)
            if geocode:
                locationArr.append({
                    "Location": region,
                    "lat"     : geocode.latitude,
                    "lon"     : geocode.longitude
                })
    else:
        geocode = geolocator.geocode(country)
        if geocode:
            locationArr.append({
                "Location": country,
                "lat"     : geocode.latitude,
                "lon"     : geocode.longitude
            })

url = f'https://api.darksky.net/forecast/{key}'


test_time = '1544270400'

test_location = locationArr[0]

get_darksky_response(url=api_url(key, test_location["lat"], test_location["lon"], test_time), _date=test_time)
