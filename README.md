# 배우다 - Beauda - Learn - Apprendre

This script 'baeuda', allow to get the content of markdown file tables and add that content to Anki cards in deck(s) 


## :package: Installation

pandoc is required on you system to allow to convert html content into markdown

### Requirements 

* python 3.8+
* httpx
* pypandoc
* beautifulsoup4

### Install the project

create a virtualenv

```bash
python3.8 -m venv baeuda
cd baeuda
source bin/activate
```

clone the project

```bash
git clone https://git.afpy.org/foxmask/baeuda
cd baeuda
```
or 
```bash
pip install baeuda
```

### Settings

edit `settings.py`

```
FOLDER = '/home/foxmask/MyNotes/Kimchi!'   # from which folder does baeuda read the notes to create into anki ?
PYPANDOC_MARKDOWN = 'markdown_github'
FILTER = ''
ANKI_URL = 'http://localhost:8765/'   # url provided by AnkiConnect https://ankiweb.net/shared/info/2055492159
ANKI_MODEL = 'Korean (foxmask)'  # the name of the model you create in Anki desktop, or the standard one you duplicate
ANKI_FIELD_COUNT = 3   # number of columns to grab from a markdown table
ANKI_FIELDS = ['Coréen', 'Romanisation', 'Français']  # put the name of the fields you want to use with the "ANKI_MODEL"
ANKI_DECK = 'Korean Courses'
```



## :dvd: DataSource

### Markdown files

The name of the file should have to be that way:

`foobar - xxx - yyy.md`

for example 

`Kimchi! 01 - insa - 인사.md`

Baeuda will create note with xxx and yyy as tag in anki. 
In our example : `insa` and `인사` 

## Format of notes for Anki 

To process, all the markdown files should have, at least, those content structure:

* h1 with the title of your markdown file
* h2 with tags name (optional) 
* table with same headers name of the "fields" defined in the "anki type of note"

Let's see with an example :

In anki, among the provided types of notes, you can find "basic" which content 2 fields "recto" and "verso"

so in your markdown file you will have to create tables with headers named *recto* and *verso* 


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


## Anki desktop

To add cards to Anki, you need to use an existing model (also known as "type of notes") 

There are many models you can use, if none fit your needs, you can create on as I did : 
`tools > type of notes` then `add` button and choose `Duplicate Basic (and reversed card)` then we'll add a third fields `Romanisation` and will change `Front` to `Coreen` and `Back` to `Français`

Then add this addon [AnkiConnect](https://foosoft.net/projects/anki-connect/index.html#installation) to allow Anki to allow us to add the notes with the current script.



## Let's Go 

First of all, start Anki on your desktop

### simulated process

```bash
python baeuda/run.py -a report
```
will display a table of all the grabbed data to create card


### creating cards

```bash
python baeuda/run.py -a go
```

during the execution, you can have a look in anki and see the decks created and receiving cards ;)


## From Markdown file to Anki in images

2) baeuda running in the console 

![Anki integration](/anki_integration.png)

3) Anki with the new created decks

![Anki Decks List](/anki_list_decks.png)

4) the cards of the deck

![Anki The Deck](/anki_deck.png)

5) one card 

![Anki The card](/anki_card.png)


(Image credits to [Emojipedia](https://emojipedia.org/))
