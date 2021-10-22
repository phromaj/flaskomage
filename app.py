from bson import json_util
from flask import Flask, request, jsonify
import pymongo

from wiki_scraper import scrape_fromages, scrape_regions

app = Flask(__name__)

username = 'lucas'
password = 'gauvain'
client = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.qfqkw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.flaskomage
fromages_coll = db.fromages
regions_coll = db.regions


@app.route('/regions', methods=['GET'])
def get_regions():
    """
    Retrieves all data from the regions collection.
    :return: regions[]: list of regions and status code 200
    """
    regions = list(regions_coll.find({}))
    return json_util.dumps(regions), 200


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
    Retrieves all data from the cheese collection.
    :return: fromages[]: list of fromages and status code 200
    """
    fromages = list(fromages_coll.find({}))
    return json_util.dumps(fromages), 200


@app.route('/fromages_filter', methods=['GET'])
def get_filter():
    try:
        fromages_data = []
        nom = {"nom": {"$regex": request.args.get("nom")}}
        # departement = {"departement": request.args.get("departement").capitalize()}
        get_value = fromages_coll.find(nom)
        for x in get_value:
            fromages_data.append(x)
    except:
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
    fromages_coll.insert_many(fromages_to_send).inserted_ids
    return "Fromages Collection generated", 200


@app.route('/fromages', methods=['POST'])
def insert():
    """
    Function to insert one or many documents in the cheese collection.
    :return: Status code 200
    """
    if not request.is_json:
        return "Il manque le JSON dans la requête", 400

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
            return "Il manque le paramètre 'nom' dans la requête", 400
        if not departement:
            return "Il manque le paramètre 'departement' dans la requête", 400
        if not isinstance(departement, list):
            return "Le type attendu pour le paramètre 'departement' n'est pas correct, il faut un tableau de string", 400
        if not pate:
            return "Il manque le paramètre 'pate' dans la requête", 400
        if not lait:
            return "Il manque le paramètre 'lait' dans la requête", 400
        if not annee_aoc:
            return "Il manque le paramètre 'annee_aoc' dans la requête", 400
        if type(annee_aoc) is int:
            if annee_aoc < 1900 or annee_aoc > 2100:
                return "L'année rentrée n'est pas valide", 400
        else:
            return "Le type attendu pour le paramètre 'annee_aoc' n'est pas correct, il faut entrer un entier"

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
def delete_many():
    """
    Function to delete all the documents in the cheese collection.
    :return: Status code 200
    """
    result = fromages_coll.delete_many({})
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
    new_values = {"$set": request.get_json()}
    fromages_coll.update_one(filter_by_id, new_values)
    return "Update", 200
