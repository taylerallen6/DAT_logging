import requests
import json
from pprint import pprint
import time
import random
import string 
from geopy.geocoders import Nominatim
import token_dat1
import sys
from datetime import datetime, timedelta


def check_token(func, kwargs):
  try:
    r = func(kwargs)
    return r
  
  except Exception as e:
    print("ERROR: ", e)
    token_dat1.save_token()

    try:
      r = func(kwargs)
      return r

    except Exception as e:
      print("NON-TOKEN ERROR!")
      print("ERROR: ", e)
      sys.exit()


def get_config_token():
  config_token = None
  with open('config_token.json', 'r') as file:
    config_token = file.read()
    config_token = json.loads(config_token)
  
  return config_token


def get_lat_long(city, state):
  query = "{}, {}".format(city, state)
  # user_agent_val = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 20)))
  geolocator = Nominatim(user_agent='routing')
  location = geolocator.geocode(query)
  print(location)

  return location.latitude, location.longitude


def get_loads(location, origin_or_dest="origin", earliest_date=None):
  temp_kwargs = locals()

  def temp(kwargs):
    location['city'] = location['city'].lower()
    location['state'] = location['state'].upper()
    location['latitude'], location['longitude'] = get_lat_long(location['city'], location['state'])

    if earliest_date != None:
      dt = datetime.strptime(kwargs['earliest_date'], "%Y-%m-%dT%H:%M")
      earliest_dt = dt.isoformat() + 'Z'
      latest_dt = (dt + timedelta(days=3)).isoformat() + 'Z'

    config_token = get_config_token()

    base_url = "https://freight.api.prod.dat.com"
    endpoint = '/search/v1/loads'
    url = base_url + endpoint
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config_token["DAT_TOKEN"]
    }
    payload = {
      "criteria": {
        "desiredSpecs": {
          "equipmentTypes": ["V"],
          "capacity": "BOTH",
        },
        "maxAgeInMinutes": 5940,
        "availability": {}
      }
    }

    if origin_or_dest == "origin":
      payload['criteria']['origin'] = {
          "point": {
            "city": location['city'],
            "state": location['state'],
            "latitude": location['latitude'],
            "longitude": location['longitude'],
            "deadhead": { "miles": 150 }
          },
        }
    elif origin_or_dest == "destination":
      payload['criteria']['destination'] = {
          "point": {
            "city": location['city'],
            "state": location['state'],
            "latitude": location['latitude'],
            "longitude": location['longitude'],
            "deadhead": { "miles": 150 }
          },
        }

    payload = json.dumps(payload)
    r = requests.post(url, headers=headers, data=payload)
    
    if r.status_code < 200 or r.status_code > 299:
      pprint(r.json())

    r = r.json()

    search_id = r['id']

    url = 'https://freight.api.prod.dat.com/search/v1/loads/{}/matches'.format(search_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config_token["DAT_TOKEN"]
    }
    params = {
      'lobackMinutes': 1440,
      'limit': 1000
    }

    r = requests.get(url, headers=headers, params=params)
    r = r.json()
    # pprint(r)

    return r

  r = check_token(temp, temp_kwargs)

  return r


# loads = get_loads('atlanta', 'ga')
# print("load count: ", len(loads))
# print()

# def get_rate_if_exists(loads):
#   try:
#     return load['rate']['baseRate']['amount']
#   except:
#     return None

# for load in loads[:]:
#   # print("################################################\n")
#   # pprint(load)
#   rate = get_rate_if_exists(load)
#   if rate:
#     print(rate)
#   # print()