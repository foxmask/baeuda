# 배우다 - Learn - Apprendre

This script 'baeuda', allow to get the content of Joplin notes with tables and add that content to Anki cards in deck(s) 


## :package: Installation


pandoc is required on you system to allow to convert html content into markdown

### Requirements 

* python 3.6+
* httpx
* joplin_api
* pypandoc
* beautifulsoup4

## :dvd: Database

### Joplin

you can use [Joplin](https://joplinapp.org/) as source of data but launching the joplin desktop version or joplin server headless

* If you use Joplin, the title of the notes should have to be that way:
`foobar - xxx - yyy` 

### Markdown files

Baeuda will drop the first part before the - and will use xxx and yyy as tag in anki

* If you use markdown file, the name of the file should have to be that way:

`foobar - xxx - yyy.md`

Baeuda will drop the first part before the - and will use xxx and yyy as tag in anki


## Format of notes for Anki 

One thing to keep in mind, to make all that stuff working all together: 

You need to have the *same header name* in your joplin tables as in the "fields" of the "anki type of note"

Let's see with an example :

In anki, among the the provided types of notes, you can find "basic" which content 2 fields "recto" and "verso"

so in joplin you will have to create tables with headers recto and verso 


```
Title of the note - Topic - details

Recto | Verso 
-------- | --------
Color on the sun ? | Yellow
Universal reply ? | 42
```

real example with three columns
```
Kimchi! Fiche 1 - 인사 - insa - salutations
Coréen | Romanisation | Français
------ | ------------ | --------
안녕하세요 | annyeonghaseyo | bonjour

```

the script will split the title of the note at each ' - ' (with space arround - ) and drop the first piece, here 'Kimchi! Fiche 1', as we don't need the name of the chapter.


## Anki desktop

To add cards to Anki, you need to use an existing model (also known as "type of notes") 

There are many models you can use, if none fit your needs, you can create on as I did : 
`tools > type of notes` then `add` button and choose `Duplicate Basic (and reversed card)` then we'll add a third fields `Romanisation` and will change `Front` to `Coreen` and `Back` to `Français`

Then add this addon [AnkiConnect](https://foosoft.net/projects/anki-connect/index.html#installation) to allow Anki to allow us to add the notes with the current script.


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
TOKEN = ''    # provide the JOPLIN TOKEN you have on the webclipper configuration page
FOLDER = 'Kimchi!'   # from which folder does baeuda read the notes to create into anki ?
PYPANDOC_MARKDOWN = 'markdown_github'
FILTER = ''
ANKI_URL = 'http://localhost:8765/'   # url provided by AnkiConnect https://ankiweb.net/shared/info/2055492159
ANKI_MODEL = 'Korean (foxmask)'  # the name of the model you create in Anki desktop, or the standard one you duplicate
ANKI_FIELD_COUNT = 3   # number of columns to grab from a joplin table
ANKI_FIELDS = ['Coréen', 'Romanisation', 'Français']  # put the name of the fields you want to use with the "ANKI_MODEL"
ONE_DECK_PER_NOTE = False    # will create one deck, set to True if you want one Deck per note

```

## Let's Go 

just before running that command
```
python baeuda/anki.py 
```
Start Joplin (with the joplin desktop or joplin headless) and Anki on your desktop

during the execution, you can have a look in anki and see the decks created and receiving cards ;)


## From Joplin to Anki in images

1) Joplin notes

![Joplin notes](/joplin_notes.png)

2) baeuda running in the console 

![Anki integration](/anki_integration.png)

3) Anki with the new created decks

![Anki Decks List](/anki_list_decks.png)

4) the cards of the deck

![Anki The Deck](/anki_deck.png)

5) one card 

![Anki The card](/anki_card.png)


(Image credits to [Emojipedia](https://emojipedia.org/))
