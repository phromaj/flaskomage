from flask import Flask, request
import pymongo
from wiki_scraper import scrape_fromages, scrape_regions

app = Flask(__name__)

username = 'lena'
password = 'admin'
client = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@coding.mvpr0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = client.flaskomage
fromages_coll = db.fromages
regions_coll = db.regions


@app.route('/get_fromages', methods=['GET'])
def get_fromages():
    fromages_data = []
    get_value = fromages_coll.find()
    for x in get_value:
        fromages_data.append(x)
    return f"{fromages_data}"


@app.route('/get_regions', methods=['GET'])
def get_regions():
    regions_data = []
    get_value = regions_coll.find()
    for x in get_value:
        regions_data.append(x)
    return f"{regions_data}"


@app.route('/scrape_regions', methods=['POST'])
def generate_regions():
    regions_to_send = scrape_regions()
    regions_coll.remove()
    insert_value = regions_coll.insert_many(regions_to_send).inserted_ids
    return str(insert_value)


@app.route('/scrape_fromages', methods=['POST'])
def generate_fromages():
    fromages_to_send = scrape_fromages()
    fromages_coll.remove()
    insert_value = fromages_coll.insert_many(fromages_to_send).inserted_ids
    return str(insert_value)


@app.route('/insert_one', methods=['POST'])
def insert_one():
    """
    Function to insert a document in the cheese collection.
    :return: 
    """
    if not request.is_json:
        return "Il manque le JSON dans la requête", 400

    nom = request.json.get('nom', None)
    departement = request.json.get('departement', None)
    pate = request.json.get('pate', None)
    lait = request.json.get('lait', None)
    annee_aoc = request.json.get('annee_aoc', None)
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

    req_data = request.get_json()
    fromage = {
        "nom": req_data["nom"],
        "departement": req_data["departement"],
        "pate": req_data["pate"],
        "lait": req_data["lait"],
        "annee_aoc": req_data["annee_aoc"],
        "fromage_id": fromages_coll.find().count() + 1,
    }
    new_fromage = fromages_coll.insert_one(fromage).inserted_id
    return f"Inserted {new_fromage}"


@app.route('/insert_many', methods=['POST'])
def insert_many():
    """
    Function that allows to insert many documents in the cheese collection.
    :return:
    """
    req_data = request.get_json()
    fromage_tab = []
    initial_count = fromages_coll.find().count()
    for data in req_data:
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
    new_fromages = fromages_coll.insert_many(fromage_tab).inserted_ids
    return f"Inserted {new_fromages}"


@app.route('/delete_one/<id_fromage>', methods=['DELETE'])
def delete_one(id_fromage):
    """
    Function to delete a cheese designated by its id.
    :return:
    """
    fromages_coll.delete_one({
        "fromage_id": int(id_fromage)
    })
    return "Delete"


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
