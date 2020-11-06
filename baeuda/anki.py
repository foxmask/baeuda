import asyncio
from bs4 import BeautifulSoup
import json
import settings
import httpx
from rich import console

console = console.Console()


def check_datasource():
    return True if settings.DATASOURCE in ('Joplin', 'MdFile') else False


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
    main loop
    """
    if check_datasource() is False:
        console.print('배우다 : the source of your notes is unknown, choose "MdFile" or "Joplin"', style="red")
        exit(0)
    klass = getattr(__import__('datasource.' + settings.DATASOURCE.lower(),
                               fromlist=[settings.DATASOURCE]), settings.DATASOURCE)
    all_data = await klass().data()

    with httpx.Client() as client:
        lines = ()
        for line in all_data:
            soup = BeautifulSoup(line['body'], 'html.parser')
            if hasattr(soup.h1, 'text'):
                # if ONE_DECK_PER_NOTE is True, will create a deck per not
                # otherwise will put everything in one deck
                # but with tags gotten from the title of the note ;)
                deck_name = soup.h1.text if settings.ONE_DECK_PER_NOTE else await klass().my_folder()
                data = anki_create_deck(deck_name=deck_name)
                data = json.dumps(data)
                tags = line['title'].split(' - ')[1:]

                res = client.post(url=settings.ANKI_URL, data=data)
                if res.status_code == 200:
                    tables = soup.find_all('table')
                    for table in tables:
                        table_lines = table.find_all('td')
                        i = 0
                        headers = ()
                        for line2 in soup.table.thead.find_all('th'):
                            if line2.text in settings.ANKI_FIELDS:
                                headers += (line2.text,)
                        if len(headers) == settings.ANKI_FIELD_COUNT:
                            lines = ()
                            i = 0

                        for line3 in table_lines:
                            if i == settings.ANKI_FIELD_COUNT:
                                i = 0
                                fields = dict(zip(headers, lines))
                                console.print(f"{fields} {tags}", style="blue")
                                data = anki_add_note(deck_name, *tags, **fields)
                                data = json.dumps(data, indent=4)
                                res = client.post(url=settings.ANKI_URL, data=data)
                                if res.status_code != 200:
                                    console.print(res.status_code, style="red")

                                lines = ()
                            i += 1
                            lines += (line3.text, )

if __name__ == '__main__':
    console.print('배우다 : starting', style="green")
    asyncio.run(anki())
    console.print('배우다 : finished', style="green")
