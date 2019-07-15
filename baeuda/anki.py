import asyncio
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


async def myfolder():
    """

    :return: the folder id
    """
    res = await joplin.get_folders()
    for line in res.json():
        if settings.FOLDER == line['title']:
            return line['id']
        if 'children' in line:
            folder_id = subfolder(line)
            if folder_id is not None:
                return folder_id


async def my_data():
    """

    :return: list of notes
    """
    data = []
    folder_id = await myfolder()
    notes = await joplin.get_folders_notes(folder_id)
    for note in notes.json():
        if settings.FILTER in note['title'] and note['is_todo'] == 0:
            content = pypandoc.convert_text(source=note['body'],
                                            to='html',
                                            format=settings.PYPANDOC_MARKDOWN)
            data.append({'title': note['title'], 'body': content})
    return data


def anki_create_deck(deck_name):
    """
    :param deck_name: string deck name
    :return data
    """
    data = {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    }
    return data


def anki_add_note(deck_name, *tags, **fields):
    """
    :param deck_name: string deck name
    :param tags: arg of strings
    :param fields: kwargs
    :return data kwargs
    """
    data = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
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


async def anki():
    """

    """
    data = await my_data()
    for line in data:
        print(line['title'])
        soup = BeautifulSoup(line['body'], 'html.parser')
        if hasattr(soup.h1, 'text'):
            # if ONE_DECK_PER_NOTE is True, will create a deck per not
            # otherwise will put everything in one deck
            # but with tags gotten from the title of the note ;)
            deck_name = soup.h1.text if settings.ONE_DECK_PER_NOTE else settings.FOLDER
            data = anki_create_deck(deck_name=deck_name)
            data = json.dumps(data)
            tags = line['title'].split(' - ')[1:]
            res = requests.post(url=settings.ANKI_URL, data=data)
            if res.status_code == 200:
                tables = soup.find_all('table')
                for table in tables:
                    tds = table.find_all('td')
                    i = 0
                    headers = ()
                    for line2 in soup.table.thead.find_all('th'):
                        if line2.text in settings.ANKI_FIELDS:
                            headers += (line2.text,)
                    if len(headers) == settings.ANKI_FIELD_COUNT:
                        lines = ()
                        i = 0

                    for line3 in tds:
                        if i == settings.ANKI_FIELD_COUNT:
                            i = 0
                            fields = dict(zip(headers, lines))
                            print(fields, tags)
                            data = anki_add_note(deck_name, *tags, **fields)
                            data = json.dumps(data, indent=4)
                            res = requests.post(url=settings.ANKI_URL, data=data)
                            if res.status_code != 200:
                                print(res.status_code)

                            lines = ()
                        i += 1
                        lines += (line3.text, )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(anki())
    loop.close()
