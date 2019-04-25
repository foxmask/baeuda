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
    

def anki_add_note(deckName, *tags, **fields):
    """
    :param deckName: string deck name
    :param tags: arg of strings
    :param fields: kwargs
    :return data kwargs
    """
    data = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deckName,
                "modelName": settings.ANKI_MODEL,
                "fields": fields,
                "options": {
                    "allowDuplicate": False
                },
                "tags": tags
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
        if hasattr(soup.h1, 'text'):
            # if ONE_DECK_PER_NOTE is True, will create a deck per not
            # otherwise will put everything in one deck
            # but with tags gotten from the title of the note ;)
            deckName = soup.h1.text if settings.ONE_DECK_PER_NOTE else settings.FOLDER
            data = anki_create_deck(deckName=deckName)            
            data = json.dumps(data)
            tags = line['title'].split(' - ')[1:]
            res = requests.post(url=settings.ANKI_URL, data=data)
            if res.status_code == 200:
                i = 0
                headers = ()
                for line in soup.table.thead.find_all('th'):
                    if line.text in settings.ANKI_FIELDS:
                        headers += (line.text,)
                if len(headers) == settings.ANKI_FIELD_COUNT:
                    lines = ()
                    i = 0
                    for line in soup.table.tbody.find_all('td'):
                        if i == settings.ANKI_FIELD_COUNT:
                            i = 0
                            fields = dict(zip(headers, lines))
                            data = anki_add_note(deckName, *tags, **fields)
                            data = json.dumps(data, indent=4)
                            print(data)
                            res = requests.post(url=settings.ANKI_URL, data=data)
                            lines = ()                    
                        i += 1
                        lines += (line.text, )

if __name__ == '__main__':
    anki(data=data())

