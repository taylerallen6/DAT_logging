import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from pprint import pprint
from datetime import datetime
import json

cred = credentials.Certificate("firebaseServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

start_date = datetime.strptime("2021-06-28 4", "%Y-%m-%d %H")
end_date = datetime.strptime("2021-06-28 6", "%Y-%m-%d %H")

docs = db.collection(u'loads').where('timestamp', '>=', start_date).where('timestamp', '<', end_date).stream()

loads = []
for doc in docs:
  data = {
    'doc_id': doc.id,
    'doc_data': doc.to_dict()
  }

  loads.append(data)

  # pprint(doc.to_dict())

# pprint(loads)

def myconverter(o):
  return o.__str__()

with open('load_data1.json', 'w') as f:
  json.dump(loads, f, default=myconverter)