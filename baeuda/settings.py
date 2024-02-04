# from which folder does baeuda read the note to create into anki ?
# FOLDER = '/home/foxmask/MesNotes/Corée🇰🇷/공부/Kimchi!/'
# FOLDER = '/home/foxmask/MesNotes/Corée🇰🇷/공부/Cours - Active Korean 1 - 2020-2021'
# FOLDER = '/home/foxmask/MesNotes/Corée🇰🇷/공부/Cours - Active Korean 2 - 2021-2022'
# FOLDER = '/home/foxmask/MesNotes/Corée🇰🇷/공부/Cours - Active Korean 3 - 2022-2023'
FOLDER = '/home/foxmask/MesNotes/Corée🇰🇷/공부/Cours - Active Korean 4 - 2023-2024'
# FOLDER = '/path/to/your/markdown/files'
# PYPANDOC_MARKDOWN = 'markdown_github'
PYPANDOC_MARKDOWN = 'gfm'

ANKI_URL = 'http://localhost:8765/'   # url provided by AnkiConnect https://ankiweb.net/shared/info/2055492159

# anki deck name is made by the first H1 of the Markdown
# anki deck are named : "Book name - Unit X - unit title"
#
# ANKI_DECK = 'Active Korean 3 - Unit 1'

ANKI_MODEL = "Korean (2 colonnes foxmask)"  # Coréen / Français
ANKI_FIELD_COUNT = 2   # number of columns to grab from a markdown table
ANKI_FIELDS = ['Coréen', 'Français', ]  # put the name of the fields you want to use with the "ANKI_MODEL"

# ANKI_MODEL = 'Korean (foxmask)'  # fields are front/back/romanisation
# ANKI_FIELD_COUNT = 3   # number of columns to grab from a markdown table
# ANKI_FIELDS = ['Coréen', 'Romanisation', 'Français']

DATASOURCE = 'MdFile'  # MdFile
