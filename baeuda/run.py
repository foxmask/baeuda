# coding: utf-8
import argparse
import asyncio
import os.path
from bs4 import BeautifulSoup
from datasource.mdfile import MdFile
import json
import settings
import httpx
from rich import console

console = console.Console()


def check_datasource():
    return True if settings.DATASOURCE in ('MdFile', ) else False


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


def anki_remove_deck(deck_name):
    data = {
        "action": "deleteDecks",
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


async def go(my_file=''):
    """
    main loop
    """
    all_data = await MdFile().data(my_file)
    with httpx.Client() as client:
        lines = ()
        for line in all_data:
            soup = BeautifulSoup(line['body'], 'html.parser')
            if hasattr(soup.h1, 'text'):
                anki_deck_name = soup.h1.text.strip()
                console.print(anki_deck_name, style="cyan")
                tags = ''
                if hasattr(soup.h2, 'text'):
                    tags = soup.h2.text if "tags:" in soup.h2.text else ""

                data = anki_create_deck(deck_name=anki_deck_name)
                data = json.dumps(data)

                res = client.post(url=settings.ANKI_URL, data=data)
                if res.status_code == 200:
                    tables = soup.find_all('table')
                    for table in tables:
                        table_lines = table.find_all('td')
                        i = 0
                        headers = ()
                        for line2 in soup.table.thead.find_all('th'):
                            # check the header is as expected in the settings
                            if line2.text in settings.ANKI_FIELDS:
                                headers += (line2.text,)
                        if len(headers) == settings.ANKI_FIELD_COUNT:
                            lines = ()
                            i = 0

                        for line3 in table_lines:
                            i += 1
                            lines += (line3.text, )
                            if i == settings.ANKI_FIELD_COUNT:
                                i = 0
                                fields = dict(zip(headers, lines))
                                if fields:
                                    console.print(f"{fields} {tags}", style="blue")
                                    # add note to card
                                    data = anki_add_note(anki_deck_name, *tags, **fields)
                                    data = json.dumps(data, indent=4)
                                    # submit the card to Anki
                                    res = client.post(url=settings.ANKI_URL, data=data)
                                    if res.status_code != 200:
                                        console.print(res.status_code, style="red")
                                    else:
                                        result = res.json()
                                        if result['result'] is None and 'error' in result:
                                            console.print(res.json(), style="red")
                                lines = ()

                    if len(tables) == 0:
                        # drop empty deck created for nothing
                        anki_remove_deck(anki_deck_name)

                elif res.status_code == 404:
                    print("AnkiConnect service not started")


async def report(my_file=''):
    """
    main loop
    """
    all_data = await MdFile().data(my_file)
    lines = ()
    for line in all_data:
        soup = BeautifulSoup(line['body'], 'html.parser')
        if hasattr(soup.h1, 'text'):
            anki_deck_name = soup.h1.text.strip()
            console.print(anki_deck_name, style="cyan")
            tags = soup.h2.text if "tags:" in soup.h2.text else ""
            tables = soup.find_all('table')
            for table in tables:
                table_lines = table.find_all('td')
                i = 0
                headers = ()

                for line2 in table.thead.find_all('th'):
                    if line2.text in settings.ANKI_FIELDS:
                        headers += (line2.text,)

                if len(headers) == settings.ANKI_FIELD_COUNT:
                    lines = ()
                    i = 0

                for line3 in table_lines:
                    i += 1
                    lines += (line3.text, )
                    if i == settings.ANKI_FIELD_COUNT:
                        i = 0
                        fields = dict(zip(headers, lines))
                        if fields:
                            console.print(f"{fields} {tags}", style="yellow")
                        lines = ()


if __name__ == '__main__':
    console.print('배우다 : Start processing ', style="green")

    if check_datasource() is False:
        console.print('배우다 : the source of your notes is unknown, set DATASOURCE="MdFile" in the settings.py file',
                      style="red")
        exit(0)

    parser = argparse.ArgumentParser(prog="python run.py", description='배우다 - baeuda')
    parser.add_argument('-a',
                        action='store',
                        choices=['report', 'go'],
                        required=True,
                        help="Choose -a report to display the content of the data that will add cards "
                             "or -a go to create the cards")
    parser.add_argument('-o', '--file', nargs='?')
    args = parser.parse_args()
    if 'a' not in args:
        parser.print_help()
    elif args.a == 'go':
        if args.file:
            if os.path.exists(args.file):
                my_file = args.file
                asyncio.run(go(my_file=my_file))
            else:
                console.print("file does not exist", style="red")
        else:
            asyncio.run(go())
    elif args.a == 'report':
        console.print('[cyan]Report[/]')
        if args.file:
            if os.path.exists(args.file):
                my_file = args.file
                asyncio.run(report(my_file=my_file))
            else:
                console.print("file does not exist", style="red")
        else:
            asyncio.run(report())

    console.print('배우다 : finished', style="green")
