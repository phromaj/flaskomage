from flask import Flask
import pymongo
from pymongo import collection

app = Flask(__name__)

username = 'lucas'
password = 'gauvain'
client = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.qfqkw.mongodb.net/?retryWrites=true&w=majority"
)
db = client.flaskomage
fromages_coll = db.fromages
regions_coll = db.regions

@app.route('/users', methods=['POST', 'GET'])
def gangngegwe():
    return f"bondou"
