from pymongo import MongoClient
import pprint
client = MongoClient(host="localhost", port=27017)

db = client.song
for STs in db.song_info.find():
     pprint.pprint(STs)
