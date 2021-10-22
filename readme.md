# Flaskomage

API développée en Flask avec le support d'une base MongoDB.

Cette API utilise les données de wikipedia.

## Mise en place de l'environnement 
Cloner le repo puis l'ouvrir. Il faudra ensuite créer un environnement et installé et les paquets requis (requirements.txt) avec la commande `pip install -r requirements.txt`
Pour lancer le serveur : `flask run`
Par défaut, vous pouvez y accéder depuis le localhost au port 5000. (localhost:5000)

Il y aura 2 collections (peut emmener à évoluer) :

- fromages
- regions

Les documents de la collection fromages seront sous cette forme :

```JSON
{
  "_id": 0,
  "nom": "",
  "departement": "",
  "pate": "",
  "lait": "",
  "annee_aoc": 0,
  "fromage_id": 0
} 
```

Les documents de la collection régions seront sous cette forme :

```JSON
{
  "_id": 0,
  "nom": "",
  "chef_lieu": "",
  "departements": [
    ""
  ],
  "superficie": "",
  "population": "",
  "code": 0,
  "region_id": 0
} 
```

## Lister toutes les données - GET

* Récupérer toutes les données sans filtres :

```py
@app.route('/fromages', methods=['GET'])
```

```py
@app.route('/regions', methods=['GET'])
```

* Récupérer toutes les données avec filtres :

```py
@app.route('/fromages', methods=['GET'])
def param():
    nom = request.args.get('nom')
    departement = request.args.get('departement')
    pate = request.args.get('pate')
    lait = request.args.get('lait')
    fromage_id = request.args.get('fromage_id')
```

```py
@app.route('/regions', methods=['GET'])
def param():
    nom = request.args.get('nom')
    chef_lieu = request.args.get('chef_lieu')
    departements = request.args.get('departements')
    region_id = request.args.get('region_id')
```

Réponse : JSON de type object[]

## Créer un document dans la collection fromages - POST

```py
@app.route('/fromages', methods=['POST'])
```

Réponse : Status 200 OK

## Modifier un document dans la collection fromages - PUT

```py
@app.route('/fromages/<id>', methods=['PUT'])
```

Response : Status 200 OK

## Supprimer un document dans la collection fromages - DELETE

```py
@app.route('/fromages/<id>', methods=['DELETE'])
```

Response : Status 200 OK
