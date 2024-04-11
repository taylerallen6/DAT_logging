import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime
from pytz import timezone

cred = credentials.Certificate("firebaseServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
batch = db.batch()

data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
df = pd.DataFrame.from_dict(data)

for index, row in df.iterrows():
  data = row.to_dict()

  timestamp = datetime.now()
  timestamp = timestamp.astimezone(timezone('US/Central'))
  data['timestamp'] = timestamp

  doc_ref = db.collection('tests').document()
  batch.set(doc_ref, data)

batch.commit()