from flask import Flask, request
import pymongo

app = Flask(__name__)

username = 'lena'
password = 'admin'
client = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@coding.mvpr0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = client.flaskomage
fromages_coll = db.fromages
regions_coll = db.regions


@app.route('/get', methods=['GET'])
def get():
    fromages_data = []
    get_value = fromages_coll.find()
    for x in get_value:
        fromages_data.append(x)
    return f"{fromages_data}"


@app.route('/insert_one', methods=['POST'])
def insert_one():
    """
    Function to insert a document in the cheese collection.
    :return: 
    """
    req_data = request.get_json()
    new_fromage = fromages_coll.insert_one(req_data).inserted_id
    print(req_data)
    return f"Inserted {new_fromage}"


# Test in Postman
#     {
#     "nom": "insert_one",
#     "departement": ["insert_one"],
#     "pate": "insert_one",
#     "lait": "insert_one",
#     "annee_aoc": "insert_one",
#     "fromage_id": 0
#     }


@app.route('/insert_many', methods=['POST'])
def insert_many():
    """
    Function that allows to insert many documents in the cheese collection.
    :return:
    """
    req_data = request.get_json()
    new_fromages = fromages_coll.insert_many(req_data).inserted_ids
    print(req_data)
    return f"Inserted {new_fromages}"


# Test in Postman
# [
#     {
#     "nom": "insert_many",
#     "departement": ["insert_many"],
#     "pate": "insert_many",
#     "lait": "insert_many",
#     "annee_aoc": "insert_many",
#     "fromage_id": 0
#     },{
#      "nom": "insert_many",
#      "departement": ["insert_many"],
#      "pate": "insert_many",
#      "lait": "insert_many",
#      "annee_aoc": "insert_many",
#      "fromage_id": 0
#      },{
#      "nom": "insert_many",
#      "departement": ["insert_many"],
#      "pate": "insert_many",
#      "lait": "insert_many",
#      "annee_aoc": "insert_many",
#      "fromage_id": 0
#      }
# ]

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

# Test in Postman
#     {
#     "nom": "update_one",
#     "departement": ["update_one"],
#     "pate": "update_one",
#     "lait": "update_one",
#     "annee_aoc": "update_one",
#     "fromage_id": 0
#     }
