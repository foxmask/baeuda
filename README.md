# 배우다 - Learn - Apprendre

Ce script permet de recuperer le contenu de notes Joplin avec des tables puis d'injecter le contenu dans une Card d'un Deck


## Joplin, les notes


```
Titre de la note


Coréen | Romanisation | Français
------ | ------------ | --------
배우다 | baeuda | apprendre

```

le titre de la note devient le nom du "Paquet" et chaque ligne du tableau devient une carte

## Anki desktop

pour créer un model anki "Outils > gerer les type de notes" puis bouton "Ajouter"   et on choisi "Dupliquer Basic (and reversed card)" d'où on ajoutera un 3° champ "Romanisation", puis changera "Front" en "한국말" et "Back" en "Français" 

Ajouter [AnkiConnect](https://foosoft.net/projects/anki-connect/index.html#installation) pour permettre à Anki de fournir un acces REST.


## Installer le projet

Pour intégrer tout le toutim 

on cree un virtualenv

```
python3.6 -m venv baeuda
cd baeuda
source bin/activate
```

on clone le repo

```
git clone https://github.com/foxmask/baeuda
cd baeuda
```

on edite `settings.py`

```
JOPLIN_WEBCLIPPER = 41184  # le port du webclipper de joplin
TOKEN = ''  # le token du webclipper
FOLDER = 'Dossier à lire'
PYPANDOC_MARKDOWN = 'markdown_github'
FILTER = 'une chaine pour reduire la recherche dans FOLDER'
ANKI_URL = 'http://localhost:8765/'
ANKI_MODEL = 'Korean (foxmask)'  # nom du model qui va servir a stocker les cartes
ANKI_TAGS = 'foxmask'   # tags au pif :P
```

Demarrer Joplin et Anki desktop

Lancer la commande 

```
python baeuda/anki.py 
```

voir les logs sur l'ecran et on contemplate le resultat dans anki desktop
