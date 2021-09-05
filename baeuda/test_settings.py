# coding: utf-8

from baeuda import settings


def test_settings():

    FOLDER = settings.FOLDER
    PYPANDOC_MARKDOWN = settings.PYPANDOC_MARKDOWN
    ANKI_URL = settings.ANKI_URL
    ANKI_MODEL = settings.ANKI_MODEL
    ANKI_DECK = settings.ANKI_DECK
    ANKI_FIELD_COUNT = settings.ANKI_FIELD_COUNT
    ANKI_FIELDS = settings.ANKI_FIELDS
    DATASOURCE = settings.DATASOURCE

    assert type(FOLDER) is str
    assert type(PYPANDOC_MARKDOWN) is str
    assert type(ANKI_URL) is str
    assert type(ANKI_MODEL) is str
    assert type(ANKI_DECK) is str
    assert type(ANKI_FIELD_COUNT) is int
    assert type(ANKI_FIELDS) is list
    assert type(DATASOURCE) is str
