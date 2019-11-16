# Dashboard - An Epitech Project

## Sommaire

 1. Documentation Utilisateur
	 1. Introduction
	 2. Se connecter
	 3. Connecter un Service
	 4. Ajouter un Widget
	 5. La page Home
	 6. Liste des Services & Widgets
 2. Documentation Développeur
	 1. Introduction
	 2. Installer le projet
	 3. Arborescence
	 4. Ajouter un Service
	 5. Ajouter un Widget
	 6. Rapide tour de l'API

# Documentation Utilisateur

## Introduction
**Dashboard** est un site de gestion de **Widgets**. Il a pour but de permettre à l'utilisateur de se connecter à divers **Services** *(ex: Twitch, Yammer, météo, RSS, Twitter, ...)*.

Une fois connecté aux **Services** de son choix, il est possible d'ajouter des **Widgets** liés à ce **Service** *(ex: nombre de spectateur d'un live Twitch, dernier messages d'un groupe Yammer, température actuelle d'une ville, ...)*.

Lorsque l'utilisateur à choisi et configuré ses **Widgets**, il peut visualiser leurs informations à tout moment depuis la page **Home** du site. Les informations de ceux-ci sont actualisées en fonction de la configuration du **Widget**.

## Se connecter
Pour se connecter sur **Dashboard**, rendez-vous à l'adresse suivante: **http://localhost:3000/**

Une fois sur la page d'accueil du site, cliquez sur **Sign-up** en haut à droite de l'écran pour créer un compte. Un email ainsi qu'un mot de passe vous seront demandé.

> ASTUCE: Choisissez un mot de passe unique et complexe.

Votre compte crée, vous serez automatiquement redirigé vers la page de connection de **Dashboard**. Rentrez votre email et votre mot de passe que vous venez juste de renseigner et cliquez sur **Login**.

Félicitation, vous êtes connectés sur **Dashboard**.

## Connecter un Service
À ce stade, vous devriez être sur une page blanche avec un nouveau menu à votre gauche. Y sont présentes les pages:

 - Home
 - Services
 - Widgets

Rendez-vous sur la page **Services**.

Une fois sur la page, deux blocs devraient apparaître: un bloc **Activated Services** et un autre **Available Services**. C'est le second bloc **Available Services** qui nous intéresse.

Dans ce bloc sont présents des petits blocs carrés que nous appellerons **Cards**. Chaque **Card** représente un **Service**, avec un nom, une couleur et une image distincte.

Pour connecter un **Service**, rien de plus simple, cliquez simplement sur le bouton **Connect** du **Service** que vous souhaitez connecter.

À partir de là, deux cas sont possibles:

 1. Le **Service** que je souhaite connecter est un **Service** SANS authentification:
Dans ce cas la, pas de soucis, le **Service** se connecte tout seul et une notification verte s'affiche en haut de votre écran pour vous alerter que le **Service** à bien été connecté.

2. Le **Service** que je souhaite connecter est un **Service** AVEC authentification:
Dans ce cas la, le site va automatiquement vous rediriger vers la page d'authentification du **Service** concerné. Il vous sera alors demandé d'accepter  que l'application **Dashboard** récolte des informations liées à votre compte (toujours celui du **Service** concerné).
Libre à vous d'accepter ou pas ces conditions. Mais si vous les refusez, il vous sera alors impossible d'utiliser ce **Service** dans le cadre du site **Dashboard**.
Une fois votre décision prise, vous serez à nouveau redirigé vers le site **Dahsboard**. Si vous avez accepté les conditions, le **Service** se connecte tout seul et une notification verte s’affiche en haut de votre écran pour vous alerter que le **Service** à bien été connecté.

Vous aurez remarqué que le bloc **Activated Services** contient maintenant le **Service** connecté et que le bloc **Available Services** ne le contient plus.

Il vous sera alors possible de vous déconnecter (bouton **Disconnect**) du **Service**.

> ATTENTION: Déconnecter un **Service** depuis le site **Dashboard** ne déconnectera pas le site **Dashboard** du service en question. Cette fonctionnalité n'est pas encore disponible et il vous faudra manuellement déconnecter le site **Dashboard** de votre service.

## Ajouter un Widget
Une fois un nouveau **Service** de connecté, l'ensemble des **Widgets** qui lui sont associés deviennent disponibles. Pour les ajouter, rendez-vous sur la page **Widgets** grâce au menu à gauche de l'écran.

Une fois sur cette page, vous devriez remarquer certaines similarités avec la page **Services**. On y retrouve nos deux blocs ainsi que nos **Cards**.

Cette fois-ci, nos **Cards** ne représentes plus les **Services** disponibles mais bien les **Widgets** disponibles, de plus, la description du **Widget** est renseigné juste en dessous de son nom.

Pour ajouter un **Widget**, encore une fois rien de plus simple, cliquez simplement sur le bouton **Add** du **Widget** que vous souhaitez connecter.

Il vous sera alors demandé de configurer votre **Widget**. Pour ce faire, une boite de dialogue va  s'afficher par dessus votre écran. Celle-ci contient:

 - Le nom du **Widget** que vous êtes en train de configurer
 - Une liste de champs de configuration dépendant du **Widget** que vous êtes en train de configurer *(ex: pour le **Widget** température actuelle d'une ville: le nom de la ville souhaité)*.
 - Un champ **Timer** définissant de taux d'actualisation (en minute) du **Widget** *(ex: pour un **Timer** de 3, le **Widget** se mettra à jour toutes les 3 minutes)*.
 - Deux boutons **Cancel** et **Confirm**

Une fois tous les champs remplis, cliquez sur le bouton **Confirm**.

> INFO: Les types de champs sont variés. Ils peuvent prendre les formes suivantes:
> - Du texte
> - Un nombre
> - Une liste de choix
> - Une date (par jour, semaine, mois ou année)
> - Un encadrement de deux dates

Si tous les champs ont étés correctement remplis, le **Widget** passera dans le bloc **Activated Widgets** et disparaîtra du bloc **Available Widgets**. De plus, une notification vous alertera que le **Widget** à bien été ajouté.

Il vous sera alors possible de le re configurer (bouton **Configure**) ou de le supprimer (bouton **Remove**).

## La page Home
Bien, maintenant que vous avez connecté vos **Services** et que vous avez ajouté des **Widgets**, il est temps de les voir en oeuvre. Retournez sur la page **Home** toujours à l'aide du menu de gauche.

La magie de **Dashboard** devrait faire effet et vous devriez voir apparaître un ensemble de blocs représentant chacun un **Widget** différent. Ceux-ci gardent les mêmes codes couleur que le **Service** en question et affiches les informations imbriquées les unes dans les autres (chaque dégradé de couleur indiquant une imbrication supplémentaire).

Plusieurs actions sont possibles vis à vis de ces **Widgets**:

 1. Déplacer un **Widget**
Il suffit de maintenir appuyer sur partie haute du **Widget**  (la où figure le nom de celui-ci) et de déplacer en même temps votre souris jusqu'à l'emplacement souhaité. Une fois ceci fait, relâcher votre bouton de souris.
 
 2. Redimensionner un **Widget** 
Effectuez le même mouvement que pour déplacer un **Widget** mais cette fois-ci en appuyant sur la petite flèche dans le coin en bas à droite du **Widget**.

3. Sauvegarder les modifications
Lorsque vous aurez déplacé ou redimensionné un **Widget**, un bouton **Save Updates** apparaîtra en bas à droite de votre écran. Cliquez dessus pour mettre à jour la position ainsi que la taille de chacun de vos **Widgets**. Si vous quittez la page **Home** sans cliquer sur ce bouton, vos **Widgets** reprendront leur position et leur taille d'origine.

Voilà, vous êtes fin prêt à profiter pleinement de toutes les possibilités que vous offre **Dashboard**. Vous pourrez retrouver ci-dessous une liste mise à jour de l'ensemble des **Services** et **Widgets** disponibles sur le site.

Merci et bon **Widgetage** !

## Liste des Services & Widgets

Liste mise à jour le **16 Novembre 2019**
 - Twitch
	 - Number of viewers for a stream
	 - Most viewed streams for a game
	 - Number of stream displayed
	 - Number of followers for a streamer
	 - Events of moderation for a specific user on your channel
	 - Events of banishment for a specific user on your channel

- Intra Epitech
	- Day's activities at a specific date
	- Log netsoul for a specific duration (daily, weekly, ...)
	- Instances (activities, projects, modules) in which the student is unregistered
	- List projects done with a specific student
	- Grades of a school year

- RSS
	- List of articles in a RSS flux

- Yammer
	- Messages of a group
	- List of user's groups


# Documentation Développeur
## Introduction
Bienvenue sur la documentation développeur du projet **Dashboard**. Dans cette documentation, nous aborderons comment créer un nouveau **Service** ou un nouveau **Widget**. Si vous n'êtes pas familier avec les notions de **Service** ou de **Widget**, je vous conseille de lire dans un premier temps la documentation utilisateur du projet.

## Installer le projet
Pour installer le projet **Dashboard**, rendez-vous sur le dépôt Github suivant: **https://github.com/Julien-Leos/Dashboard**

> ATTENTION: Vous aurez besoin des packets suivants:
>  - yarn
>  - docker
>  - docker-compose

Clonez le dépôt
> git clone https://github.com/Julien-Leos/Dashboard.git

Déplacez-vous dans le dépôt
> cd Dashboard

Instanciez le projet
> docker-compose build

Lancez le projet
> docker-compose up -d

Le site **Dashboard** si situe sur le port **3000** tandisque le serveur sur le port **8080**.


## Arborescence
Avant de rentrer dans le vif du sujet, voyons ensemble comment est constitué  l'arborescence du projet:

> | app/
> | server/
> | docker-compose.yml

Le dossier **app** contient l'ensemble des vues du projet. Cette partie est développée en **Vue.js** dans une architecture **Nuxt.js**. Vous n'aurez pas à y toucher à moins de vouloir transformer en profondeur le projet. Si tel est le cas, je vous demanderez de bien vouloir **Fork** de projet depuis le lien Github. Sans quoi, un **Pull-Request** modifiant le dossier **app** sera systématiquement refusé.

Le dossier **server** contient quant à lui l'ensemble des routes d'API du projet. Il est développé en **Python** grâce au framework **Flask**. C'est cette partie et uniquement cette partie qui va contenir l'ensemble des fichiers concernants l'ensemble des **Services** et **Widgets** de **Dashboard**.

Le fichier **docker-compose.yml**  contient la configuration nécessaire à la dockerisation du projet. Vous n'aurez pas à y toucher non plus.

## Ajouter un Service
Comme vous l'aurez sans doute deviné, nous allons travailler au seins du dossier **server**. rendez-vous dans celui-ci.

Vous devriez y trouver un fichier nommé **about.json**. Ce fichier est indispensable au bon fonctionnement du projet. C'est lui qui va contenir les données brutes des chacun des **Services** et **Widgets** du **Dashboard**.

Celui-ci est organisé de la manière suivante:

```json
{
  "client": {---}, 
  "server": {
    "current_time": "---", 
    "services": [---]
  }
}
```
Seul le tableau **services** dans l'object **server** va nous intéresser. Il va contenir, comme son l'indique, l'ensemble des **Services** du projet.

Bien, ouvrons ce tableau et voyons comment est formé un **Service**:
```json
---
	{
	  "name": "---",
	  "isOauth": ---,
	  "color": "---",
	  "widgets": [---]
	}
---
```
Celui-ci est composé de quatre articles:

|Nom|Type|Description|Exemple|
|--|--|--|--|
|name|String|Nom du **Service** (en minuscule)|twitch
|isOauth|Boolean|Si le **Service** nécessite une authentification Oauth (ou Oauth2)|true
|color|String|Couleur du **Service** sous format [hexadécimal](https://fr.wikipedia.org/wiki/Couleur_du_Web#Triplet_hexad%C3%A9cimal)|6441A4
|widgets|Array|List des Widgets (voir partie **Ajouter un Widget**)| ∅

Pour ajouter un nouveau **Service**, vous l'aurez compris, il vous faudra ajouter et compléter une nouvelle entrée dans le tableau **services** du fichier **about.json**.

Une fois ceci fait, le plus gros du travail reste à faire. Pour simplifier, voici la liste des étapes à suivre:

 1. Créer un fichier **[monService].py** *(en remplacant [monService] par le nom de votre **Service** tel que renseigné dans le fichier about.json)*

 2. Copier-coller le code suivant au sein de ce fichier
```python
import requests
import json

from flask import Blueprint, request, jsonify
from flask_api import status

import app
monservice_page = Blueprint('monservice_page', __name__)

# TO-DO: Modifiez par l'id client fourni par votre Service
clientId = "123456789abcdefgh"

@monservice_page.route('/monservice/oauth', methods=["GET"])
def	oauth():
redirectUri =  "http://localhost:3000/services?from=monservice"

# TO-DO: Modifiez cette URL en fonction de la documentation de votre Service. Elle devrait normalement systématiquement contenir une URI de redirection ainsi qu'un id client.
return jsonify("https://monservice/oauth2/authorize?client_id="  + clientId +  "&redirect_uri="  + redirectUri +  "&response_type=token")


@monservice_page.route('/monservice/oauth2', methods=["POST"])
def	oauth2():
body = request.form.to_dict()

# TO-DO: Modifiez cette ligne en fonction de l'API de votre Service, de manière à récupérer l'accessToken.
accessToken = body["url"].split("#")[1].split("&")[0].split("=")[1]

app.setServiceAccesToken(body["userId"], "monservice", accessToken)
return jsonify("Oauth2: OK"), status.HTTP_200_OK
```
3. Toujours au sein de ce fichier, modifiez TOUTES les références à **monservice** par le nom de votre **Service** tel que renseigné dans le fichier about.json.

4. Effectuez l'ensembles des **TO-DO** comme décrit dans le commentaire qui suit.
> INFO: Dans la fonction **oauth2**, la variable **body** contient un attribu **url**. Celui-ci à pour valeur soit l'URL de redirection de l'API de votre **Service** (avec dans ce cas la, l'accessToken dans les paramètres de l'URL), soit dans la partie hachée de l'URL de redirection de l’API de votre **Service** (avec dans ce cas la, l'accessToken dans les paramètres de la partie hachée de l'URL).

