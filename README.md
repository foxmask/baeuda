# 배우다 - Learn - Apprendre

This script 'baeuda', allow to get the content of Joplin notes with tables and add that content to Anki cards in deck(s) 


## Joplin, format of notes


```
Title of the note - language A - Language B- language C

HeadingA | HeadingB | Heading C
-------- | -------- | ---------
cel A | cel B | cel C
```

example 
```
Kimchi! Fiche 1 - 인사 - insa - salutations
Coréen | Romanisation | Français
------ | ------------ | --------
안녕하세요 | annyeonghaseyo | bonjour

```

the script will split the title of the note at each ' - ' and drop the first piece, here 'Kimchi! Fiche 1', as we don't need the name of the chapter.


## Anki desktop

To add cards to Anki, you need to use an existing model. 
There are many models you can use, if none fit your needs, you can create on as I did : 
"tools > type of notes" then "add" button and choose "Duplicate Basic (and reversed card)" then we'll add a third fields "Romanication" and will change "Front" to "Coreen" and "Back" to "Français"

Then add this addon [AnkiConnect](https://foosoft.net/projects/anki-connect/index.html#installation) to allow Anki to provide a REST access that will allow us to add the note with the current script.


## Install the project

create a virtualenv

```
python3.6 -m venv baeuda
cd baeuda
source bin/activate
```

clone the project

```
git clone https://github.com/foxmask/baeuda
cd baeuda
```

edit `settings.py`

```
JOPLIN_WEBCLIPPER = 41184
TOKEN = '' # provide the token of Joplin you can grab from the webclipper config page
FOLDER = '🇰🇷  Kimchi!'
PYPANDOC_MARKDOWN = 'markdown_github'
FILTER = ''  # if you need to reduce the list of note you want to add , set a string here
ANKI_URL = 'http://localhost:8765/'
ANKI_MODEL = 'Korean (foxmask)' # the name of the model you create in Anki desktop
ANKI_FIELD_COUNT = 3   # number of columns to grab from a joplin notes table 
ANKI_FIELDS = ['Coréen', 'Romanisation', 'Français']  # the name of the fields from the anki model 
ONE_DECK_PER_NOTE = False # will create one deck, set to True if you want one Deck per note
```

## Let's Go 

just before running that command
```
python baeuda/anki.py 
```
Start Joplin and Anki on you desktop

during the running you can have a look in anki and see the deck created and receiving card ;)


## From Joplin to Anki in images

1) Joplin notes

![Joplin notes](/joplin_notes.png)

2) baeuda running in the console 

![Anki integration](/anki_integration.png)

3) Anki with the new created decks

![Anki Liste des Decks](/anki_list_decks.png)

4) the cards of the deck

![Anki Le Deck](/anki_deck.png)

5) one card 

![Anki Le Carte](/anki_card.png)
