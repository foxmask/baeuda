from bs4 import BeautifulSoup
from joplin_api import JoplinApi
import json
import pypandoc
import settings
import requests

joplin = JoplinApi(settings.TOKEN)

def subfolder(folder):
    """

    :param folder: subfolder
    :return: line of the founded children
    """
    for line in folder['children']:
        if settings.FOLDER == line['title']:
            return line['id']

def myfolder():
    """

    :return: the folder id
    """
    res = joplin.get_folders()
    for line in res.json():
        if settings.FOLDER == line['title']:
            return line['id']
        if 'children' in line:
            folder_id = subfolder(line)
            if folder_id is not None:
                return folder_id

def data():
    """

    :return: list of notes
    """
    data = []
    folder_id = myfolder()
    notes = joplin.get_folders_notes(folder_id)
    for note in notes.json():
        if settings.FILTER in note['title'] and note['is_todo'] == 0:
            content = pypandoc.convert_text(source=note['body'], 
                                            to='html', 
                                            format=settings.PYPANDOC_MARKDOWN)
            data.append({'title': note['title'], 'body': content})
    return data

def anki_create_deck(deckName):
    """
    :param deckName: string deck name
    :return data
    """
    data = {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deckName
        }
    }
    return data    
    

def anki_add_note(deckName, korean, french, romanisation):
    """
    :param deckName: string deck name
    :param note: dict of note
    :return data
    """
    data = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deckName,
                "modelName": settings.ANKI_MODEL,
                "fields": {
                    "한국말": korean,
                    "Français": french,
                    "Romanisation": romanisation
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": [
                    settings.ANKI_TAGS,
                ]
            }
        }        
    }
    return data

def anki(data):
    """
    :param data: string converted in html
    """
    for line in data:
        soup = BeautifulSoup(line['body'], 'html.parser')
        deckName = soup.h1.text
        print("deckName ", deckName)
        data = anki_create_deck(deckName=deckName)
        data = json.dumps(data)
        res = requests.post(url=settings.ANKI_URL, data=data)
        if res.status_code == 200:
            i = 0
            korean = romanisation = french = ''
            for line in soup.table.tbody.find_all('td'):
                i = i + 1
                if i == 4:
                    i = 1
                    print("korean ", korean, " romanisation " , romanisation, " french ", french)
                    data = anki_add_note(deckName, korean, french, romanisation)
                    data = json.dumps(data)
                    res = requests.post(url=settings.ANKI_URL, data=data)
                if i == 1:
                    korean = line.text.strip()
                if i == 3:
                    french = line.text.strip()
                if i == 2:
                    romanisation = line.text.strip()


if __name__ == '__main__':
    anki(data=data())

