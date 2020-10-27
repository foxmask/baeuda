# coding: utf-8

from baeuda import settings


def test_settings():

    JOPLIN_WEBCLIPPER = settings.JOPLIN_WEBCLIPPER
    TOKEN = settings.TOKEN
    FOLDER = settings.FOLDER
    PYPANDOC_MARKDOWN = settings.PYPANDOC_MARKDOWN
    FILTER = settings.FILTER
    ANKI_URL = settings.ANKI_URL
    ANKI_MODEL = settings.ANKI_MODEL
    ANKI_FIELD_COUNT = settings.ANKI_FIELD_COUNT
    ANKI_FIELDS = settings.ANKI_FIELDS
    ONE_DECK_PER_NOTE = settings.ONE_DECK_PER_NOTE
    DATASOURCE = settings.DATASOURCE

    assert type(JOPLIN_WEBCLIPPER) is int
    assert type(TOKEN) is str
    assert type(FOLDER) is str
    assert type(PYPANDOC_MARKDOWN) is str
    assert type(FILTER) is str
    assert type(ANKI_URL) is str
    assert type(ANKI_MODEL) is str
    assert type(ANKI_FIELD_COUNT) is int
    assert type(ANKI_FIELDS) is list
    assert type(ONE_DECK_PER_NOTE) is bool
    assert type(DATASOURCE) is str
