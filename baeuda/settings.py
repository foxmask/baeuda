# from which folder does baeuda read the note to create into anki ?
FOLDER = '/home/foxmask/MesNotes/Corée🇰🇷/공부/Kimchi!/'
# FOLDER = '/path/to/your/markdown/files'
# PYPANDOC_MARKDOWN = 'markdown_github'
PYPANDOC_MARKDOWN = 'gfm'

ANKI_URL = 'http://localhost:8765/'   # url provided by AnkiConnect https://ankiweb.net/shared/info/2055492159

ANKI_DECK = 'Kimchi!'

# ANKI_MODEL = "Korean (2 colonnes foxmask)"  # Coréen / Français
# ANKI_FIELD_COUNT = 2   # number of columns to grab from a makrdown table
# ANKI_FIELDS = ['Français', 'Coréen', ]  # put the name of the fields you want to use with the "ANKI_MODEL"


ANKI_MODEL = 'Korean (foxmask)'  # fields are front/back/romanisation
ANKI_FIELD_COUNT = 3   # number of columns to grab from a markdown table
ANKI_FIELDS = ['Coréen', 'Romanisation', 'Français']

DATASOURCE = 'MdFile'  # MdFile
