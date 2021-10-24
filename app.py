from bson import json_util
from flask import Flask, request, jsonify
import pymongo

from wiki_scraper import scrape_fromages, scrape_regions

app = Flask(__name__)

username = 'lena'
password = 'admin'
client = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@coding.mvpr0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.flaskomage
fromages_coll = db.fromages
regions_coll = db.regions


@app.route('/regions', methods=['GET'])
def get_regions():
    """
    Retrieves one or many datas from the regions collection.
    :return: regions[]: list of regions and status code 200
    """
    try:
        regions_data = []
        filter = {}
        if "region_id" in request.args:
            filter["region_id"] = int(request.args.get("region_id"))
        if "nom" in request.args:
            filter["nom"] = {"$regex": request.args.get("nom").capitalize()}
        if "departement" in request.args:
            filter["departement"] = {"$regex": request.args.get("departement").capitalize()}
        if "chef_lieu" in request.args:
            filter["chef_lieu"] = {"$regex": request.args.get("chef_lieu").capitalize()}
        if "superficie" in request.args:
            filter["superficie"] = int(request.args.get("superficie"))
        if "population" in request.args:
            filter["population"] = int(request.args.get("population"))
        if "code" in request.args:
            filter["code"] = int(request.args.get("code"))

        get_value = regions_coll.find(filter)
        for x in get_value:
            regions_data.append(x)


    except Exception as inst:
        print(inst)
        return "An error has occured", 500
    return json_util.dumps(regions_data), 200


@app.route('/regions/db_generator', methods=['POST'])
def generate_regions():
    """
    Generate datas in regions collection.
    :return: Status code 200
    """
    regions_to_send = scrape_regions()
    regions_coll.remove()
    regions_coll.insert_many(regions_to_send).inserted_ids
    return "Regions Collection generated", 200


@app.route('/fromages', methods=['GET'])
def get_fromages():
    """
    Retrieves one or many datas from the fromages collection.
    :return: fromages[]: list of fromages and status code 200
    """
    try:
        fromages_data = []
        filter = {}
        if "fromage_id" in request.args:
            filter["fromage_id"] = int(request.args.get("fromage_id"))
        if "departement" in request.args:
            filter["departement"] = {
                "$regex": request.args.get("departement").capitalize()}
        if "nom" in request.args:
            filter["nom"] = {"$regex": request.args.get("nom").capitalize()}
        if "annee" in request.args:
            filter["annee_aoc"] = int(request.args.get("annee"))
        if "pate" in request.args:
            filter["pate"] = {"$regex": request.args.get("pate")}
        if "lait" in request.args:
            filter["lait"] = {"$regex": request.args.get("lait").capitalize()}
        get_value = fromages_coll.find(filter)
        for x in get_value:
            fromages_data.append(x)
    except Exception as inst:
        print(inst)
        return "An error has occured", 500
    return json_util.dumps(fromages_data), 200


@app.route('/fromages/db_generator', methods=['POST'])
def generate_fromages():
    """
    Generate datas in fromages collection.
    :return: Status code 200
    """
    fromages_to_send = scrape_fromages()
    fromages_coll.remove()
    fromages_coll.insert_many(fromages_to_send)
    return "Fromages Collection generated", 200


@app.route('/fromages', methods=['POST'])
def insert():
    """
    Function to insert one or many documents in the cheese collection.
    :return: Status code 200
    """
    if not request.is_json:
        return "The JSON is missing in the request", 400

    fetchedDatas = request.get_json()
    fromage_tab = []
    initial_count = fromages_coll.find().count()

    if not isinstance(fetchedDatas, list):
        fetchedDatas = [fetchedDatas]

    for data in fetchedDatas:
        nom = data.get('nom', None)
        departement = data.get('departement', None)
        pate = data.get('pate', None)
        lait = data.get('lait', None)
        annee_aoc = data.get('annee_aoc', None)
        if not nom:
            return "The 'nom' parameter is missing in the query", 400
        if not departement:
            return "The parameter 'departement' is missing in the query", 400
        if not isinstance(departement, list):
            return "The expected type for the 'departement' parameter is not correct, a string array is required", 400
        if not pate:
            return "The parameter 'pate' is missing in the query", 400
        if not lait:
            return "The parameter 'lait' is missing in the query", 400
        if not annee_aoc:
            return "The parameter 'annee_aoc' is missing in the query", 400
        if type(annee_aoc) is int:
            if annee_aoc < 1900 or annee_aoc > 2100:
                return "The re-entry year is not valid", 400
        else:
            return "The expected type for the parameter 'annee_aoc' is not correct, you have to enter an integer"

        initial_count += 1
        fromage = {
            "nom": data["nom"],
            "departement": data["departement"],
            "pate": data["pate"],
            "lait": data["lait"],
            "annee_aoc": data["annee_aoc"],
            "fromage_id": initial_count,
        }
        fromage_tab.append(fromage)

    # Insert many documents in the cheese collection.
    fromages_coll.insert_many(fromage_tab).inserted_ids
    return "Successfully posted", 200


@app.route('/fromages/<id_fromage>', methods=['DELETE'])
def delete_one(id_fromage):
    """
    Function to delete a cheese designated by its id.
    :return: Status code 200
    """
    result = fromages_coll.delete_one({
        "fromage_id": int(id_fromage)
    })
    if result.deleted_count == 0:
        return "ID isn't correct", 500
    else:
        return "Deleted", 200


@app.route('/fromages', methods=['DELETE'])
def delete_many_fromages():
    """
    Function to delete all the documents in the cheese collection.
    :return: Status code 200
    """
    result = fromages_coll.delete_many({})
    if result.deleted_count == 0:
        return "Could not delete", 500
    else:
        return "Deleted", 200


@app.route('/regions', methods=['DELETE'])
def delete_many_regions():
    """
    Function to delete all the documents in the cheese collection.
    :return: Status code 200
    """
    result = regions_coll.delete_many({})
    if result.deleted_count == 0:
        return "Could not delete", 500
    else:
        return "Deleted", 200


@app.route('/fromages/<id_fromage>', methods=['PUT'])
def update_one(id_fromage):
    """
    Function to update a cheese designated by its id.
    :return: Status code 200
    """
    filter_by_id = {'fromage_id': int(id_fromage)}
    fromage = request.get_json()
    keys = ["nom", "departement", "annee_aoc", "pate", "lait"]
    for key in fromage.keys():
        if not key in keys:
            return "Sent JSON is not valid", 500
    if "annee_aoc" in fromage and type(fromage["annee_aoc"]) is not int:
        return "annee_aoc must be an int", 500
    if "departement" in fromage and not isinstance(fromage["departement"], list):
        return "departement must be a list"
    new_values = {"$set": fromage}
    fromages_coll.update_one(filter_by_id, new_values)
    return "Updated", 200
