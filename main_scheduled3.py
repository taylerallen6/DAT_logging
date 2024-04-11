import dat_api1
from pprint import pprint
from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np
import math
import sys
import json
import time
import firebase_admin
from firebase_admin import credentials, firestore
from pytz import timezone


def store_loads(db, batch, location, origin_or_dest):
  loads = dat_api1.get_loads(location, origin_or_dest)
  # pprint(loads[:2])

  loads = np.array(loads)
  load_split = len(loads) / 400
  load_split = math.ceil(load_split)
  loads_list = np.array_split(loads, load_split)

  timestamp = datetime.now()
  timestamp = timestamp.astimezone(timezone('US/Central'))

  for loads in loads_list:

    for load in loads:
      data = {
        "timestamp": timestamp,
        "load_data": load
      }

      doc_ref = db.collection('loads').document()
      batch.set(doc_ref, data)

    batch.commit()


if __name__ == "__main__":

  cred = credentials.Certificate("firebaseServiceAccountKey.json")
  firebase_admin.initialize_app(cred)

  db = firestore.client()
  batch = db.batch()

  location = {
    "city": "los angeles",
    "state": "ca"
  }

  store_loads(db, batch, location, "origin")
  store_loads(db, batch, location, "destination")