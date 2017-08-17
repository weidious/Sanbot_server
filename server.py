from pymongo import MongoClient
import json
import os
import time


client = MongoClient("mongodb://127.0.0.1:27017")
db = client['test']
collection = db.sprint
print(collection.find()[1])
