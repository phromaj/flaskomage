# Flaskomage

API développée en Flask avec le support d'une base MongoDB.

Cette API utilise les données de wikipedia.

Il y aura 2 collections (peut emmener à évoluer) : 
- fromages
- regions

Les documents de la collection fromages seront sous cette forme :
```JSON
{
    "nom": "",
    "departement": "",
    "pate": "",
    "lait": "",
    "annee_aoc": 0
} ```

Les documents de la collection régions seront sous cette forme :
```JSON
{
    "nom": "",
    "chef_lieu": "",
    "departements": [""],
    "superficie": "",
    "population": "",
    "densite": "",
    "code": 0
} ```

## Lister toutes les données - GET

@app.route('/fromages', methods=['GET'])
@app.route('/regions', methods=['GET'])

Réponse : JSON de type object[]

## Créer un document dans la collection fromages - POST

@app.route('/fromages', methods=['POST'])


Réponse : JSON of type User[] containing the newly created user.

## Modify a user - PUT

Function that allows to modify a user.

@app.route('/users/<id>', methods=['PUT'])


Response : JSON of type User[] containing the modified user.

## Delete a user - DELETE

Function that allows you to delete a user.

@app.route('/users/<id>', methods=['DELETE'])


Response : Status 200 OK