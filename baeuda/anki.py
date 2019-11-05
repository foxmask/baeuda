import asyncio
from bs4 import BeautifulSoup
import json
import settings
import httpx


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
    async with httpx.AsyncClient() as client:
        # data = await my_data()
        klass = getattr(__import__('datasource.' + settings.DATASOURCE.lower(),
                                   fromlist=[settings.DATASOURCE]), settings.DATASOURCE)
        all_data = await klass().data()
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

                res = await client.post(url=settings.ANKI_URL, data=data)
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
                                res = await client.post(url=settings.ANKI_URL, data=data)
                                if res.status_code != 200:
                                    print(res.status_code)

                                lines = ()
                            i += 1
                            lines += (line3.text, )

if __name__ == '__main__':
    print('배우다 : starting')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(anki())
    loop.close()
    print('배우다 : finished')
