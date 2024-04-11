import dat_api1
from pprint import pprint
from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np
import math
import sys
import json
import time


def get_rate_if_exists(load):
  try:
    return load['rate']['baseRate']['amount']
  except:
    return None

def filter_loads_with_rate(loads):
  new_loads = []

  for load in loads:
    if get_rate_if_exists(load):
      new_loads.append(load)

  return new_loads

def get_rate_per_mile(rate, miles):
  return rate / miles

def parse_load_id(load):
  return load['postingId']

def parse_origin(load):
  origin = load['origin']['point']
  return origin['city'] + ", " + origin['state']

def parse_dest(load):
  dest = load['destination']['point']
  return dest['city'] + ", " + dest['state']

def parse_miles(load):
  return load['tripLength']['distanceMiles']

def parse_deadhead(load):
  return load['origin']['point']['deadhead']['miles']

def parse_company_name(load):
  return load['poster']['company']

def parse_contact_info(load):
  contact_info = load['poster']['contact']
  return json.dumps(contact_info)

def parse_comments(load):
  comments = load['comments']
  return json.dumps(comments)

def parse_registry_lookup_id(load):
  return load['poster']['registryLookupId']

def parse_earliest_availability(load):
  format = "%Y-%m-%dT%H:%M:%S"
  earliest_availability = datetime.strptime(load['availability']['earliest'][:-5], format)
  format = "%Y-%m-%d %H:%M:%S"
  return earliest_availability.strftime(format)

def parse_latest_availability(load):
  format = "%Y-%m-%dT%H:%M:%S"
  latest_availability = datetime.strptime(load['availability']['latest'][:-5], format)
  format = "%Y-%m-%d %H:%M:%S"
  return latest_availability.strftime(format)

def create_df(
  load_ids,
  mileages,
  rates,
  rate_per_miles,
  deadheads,
  origins,
  dests,
  company_names,
  contact_infos,
  comments,
  registry_lookup_ids,
  earliest_availabilities,
  latest_availabilities
):

  df = pd.DataFrame({
    'load_id': load_ids,
    'mileage': mileages,
    'rate': rates,
    'rate_per_mile': rate_per_miles,
    'deadhead': deadheads,
    'origin': origins,
    'destination': dests,
    'company_name': company_names,
    'contact_info': contact_infos,
    'comments': comments_list,
    'registry_lookup_id': registry_lookup_ids,
    'earliest_availability': earliest_availabilities,
    'latest_availability': latest_availabilities,
  })

  df = df.dropna()
  df = df.sort_values(['rate'], ascending=[False]).reset_index(drop=True)
  df = df.dropna()

  return df

def create_simple_df(df):
  return df[[
    'load_id',
    'mileage',
    'rate',
    'rate_per_mile',
    'deadhead',
    'origin',
    'destination',
  ]]


if __name__ == "__main__":

  lookup_origin = {
    "city": "pittsburg",
    "state": "pa"
  }
  lookup_destination = {
    "city": "buffalo",
    "state": "ny"
  }

  # city = "memphis"
  # state = "tn"

  loads = dat_api1.get_loads(lookup_origin, lookup_destination)
  print(len(loads))
  loads = filter_loads_with_rate(loads)
  print(len(loads))

  load_ids = []
  mileages = []
  rates = []
  rate_per_miles = []
  deadheads = []
  origins = []
  dests = []
  company_names = []
  contact_infos = []
  comments_list = []
  registry_lookup_ids = []
  earliest_availabilities = []
  latest_availabilities = []
  

  for i, load in enumerate(loads[:]):
    pprint(load)
    print()

    miles = parse_miles(load)
    if miles == 0 or miles == None:
      continue

    load_id = parse_load_id(load)
    load_ids.append(load_id)

    rate = get_rate_if_exists(load)
    rate_per_mile = get_rate_per_mile(rate, miles)

    mileages.append(miles)
    rates.append(rate)
    rate_per_miles.append(rate_per_mile)
    deadheads.append(parse_deadhead(load))
    origins.append(parse_origin(load))
    dests.append(parse_dest(load))
    company_names.append(parse_company_name(load))
    contact_infos.append(parse_contact_info(load))
    comments_list.append(parse_comments(load))
    registry_lookup_ids.append(parse_registry_lookup_id(load))
    earliest_availabilities.append(parse_earliest_availability(load))
    latest_availabilities.append(parse_latest_availability(load))

  
  ### ADMIN DF
  df = create_df(
    load_ids,
    mileages,
    rates,
    rate_per_miles,
    deadheads,
    origins,
    dests,
    company_names,
    contact_infos,
    comments_list,
    registry_lookup_ids,
    earliest_availabilities,
    latest_availabilities,
  )
  # print(len(df))
  # print(df.head(20))

  ### SIMPLE DF
  simple_df = create_simple_df(df)
  print(len(simple_df))
  print(simple_df.head(20))