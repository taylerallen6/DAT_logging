import json
import requests
import config


def get_token():
  base_url = "https://identity.api.dat.com/access/v1/token/organization"
  headers = {
    'content-type': 'application/json',
  }
  payload = {
    "username": config.DAT_SERVICE_USERNAME,
    "password": config.DAT_SERVICE_PASSWORD
  }
  payload = json.dumps(payload)

  r = requests.post(base_url, data=payload, headers=headers)
  r = r.json()
  service_token = r['accessToken']

  base_url = "https://identity.api.dat.com/access/v1/token/user"
  headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer ' + service_token
  }
  payload = {
    "username": config.DAT_INDI_USERNAME,
  }
  payload = json.dumps(payload)

  r = requests.post(base_url, data=payload, headers=headers)
  r = r.json()
  indi_token = r['accessToken']

  return indi_token


def save_token():
  token = get_token()

  data = None
  with open('config_token.json', 'r') as file:
    data = file.read()
    data = json.loads(data)
    data['DAT_TOKEN'] = token

  with open('config_token.json', 'w') as file:
    data = json.dumps(data)
    file.write(data)

  print("New DAT token created")


# save_token()