from bson import json_util
from flask import Flask, request, jsonify
import pymongo

from wiki_scraper import scrape_fromages, scrape_regions

app = Flask(__name__)

username = 'lucas'
password = 'gauvain'
client = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.qfqkw.mongodb.net/?retryWrites=true&w=majority"
)
db = client.flaskomage
fromages_coll = db.fromages
regions_coll = db.regions


@app.route('/fromages', methods=['GET'])
def get():
    try:
        fromages = list(fromages_coll.find({}))
    except:
        return "An error has occured", 500
    return json_util.dumps(fromages), 200


@app.route('/scrape_regions', methods=['POST'])
def generate_regions():
    regions_to_send = scrape_regions()
    regions_coll.remove()
    try:
        regions_coll.insert_many(regions_to_send).inserted_ids
    except:
        return "Could not generate db", 500
    return "Regions Collection generated", 200


@app.route('/scrape_fromages', methods=['POST'])
def generate_fromages():
    fromages_to_send = scrape_fromages()
    fromages_coll.remove()
    try:
        regions_coll.insert_many(fromages_to_send).inserted_ids
    except:
        return "Could not generate db", 500
    return "Regions Collection generated", 200


@app.route('/fromages', methods=['POST'])
def insert():
    """
    Function to insert one or many documents in the cheese collection.
    :return: 
    """
    fetchedDatas = request.get_json()
    if not isinstance(fetchedDatas, list):
        fetchedDatas = [fetchedDatas]
    fromages_coll.insert_many(fetchedDatas).inserted_ids
    try:
        fromages_coll.insert_one(request.get_json()).inserted_id
    except:
        return "An error has occured", 500
    return "Successfully posted", 200


@app.route('/delete_one/<id_fromage>', methods=['DELETE'])
def delete_one(id_fromage):
    """
    Function to delete a cheese designated by its id.
    :return:
    """
    try:
        fromages_coll.delete_one({
            "fromage_id": int(id_fromage)
        })
    except:
        return "Could not delete element", 500
    return "Deleted", 200


@app.route('/delete_many', methods=['DELETE'])
def delete_many():
    """
    Function to delete all the documents in the cheese collection.
    :return:
    """
    fromages_coll.delete_many({})
    return "Delete"


@app.route('/update_one/<id_fromage>', methods=['PUT'])
def update_one(id_fromage):
    """
    Function to update a cheese designated by its id.
    :return:
    """
    filter_by_id = {'fromage_id': int(id_fromage)}
    new_values = {"$set": request.get_json()}
    fromages_coll.update_one(filter_by_id, new_values)
    return "Update"
