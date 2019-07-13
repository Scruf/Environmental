import json, os, time
from datetime import datetime, date, timezone
from requests import get
from dateutil.rrule import rrule, DAILY
from geocoder import arcgis



def get_darksky_response(url, _date):
    print(url)
    time.sleep(3)
    requests = get(url)
    if requests.status_code == 200:
        if requests.json().get("hourly", False):
            data = requests.json()["hourly"]
            ts = int(_date)
            _time = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            date_json = {
                str(_time):{}
            }

            for timestamp in data["data"]:
                _timestamptime = datetime.utcfromtimestamp(int(timestamp["time"])).strftime("%Y-%m-%d %H:%M:%S")
                date_json[str(_time)].update({
                _timestamptime:{
                        "temperature":timestamp["temperature"],
                        "dewPoint":timestamp["dewPoint"],
                        "humidity":timestamp["humidity"]
                    }
                })
            return date_json

    else:
        print(requests.text)
        return {}


key = "689904ed285f890e88c17672dfe9b706"



api_url = lambda key, lat, lon, time: f'https://api.darksky.net/forecast/{key}/{lat},{lon},{time}?units=us'

regions = None
with open('Invalid.json', 'r') as fil:
    regions = json.load(fil)

locationArr = []
for country in regions:
    time.sleep(2)
    # print(country.keys())
    if country["Region"]:
        for region in country["Region"]:
            geocode = arcgis(region).latlng
            if geocode:
                locationArr.append({
                    "Location": region,
                    "lat"     : geocode[0],
                    "lon"     : geocode[1]
                })
                print(region, geocode[0], geocode[1])
    else:
        try:
            geocode = arcgis(country).latlng
            if geocode:
                locationArr.append({
                    "Location": country,
                    "lat"     : geocode[0],
                    "lon"     : geocode[1]
                })
        except Exception as ex:
            pass


start_date = date(2018,1,1)
end_date = date(2018,12,31)

bigFile = []
for dt in rrule(DAILY, dtstart=start_date, until=end_date):
    _timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    for region in locationArr:
        print(_timestamp, region["Location"])
        darksky_response = get_darksky_response(url=api_url(key, region["lat"], region["lon"], int(_timestamp)), _date=_timestamp)
        bigFile.append(darksky_response)
with open("Sample.json", "w") as fil:
    json.dump(bigFile, fil)



# https://api.darksky.net/forecast/689904ed285f890e88c17672dfe9b706/-24.188129999999944,-65.29603999999995?exclude=currently,flags