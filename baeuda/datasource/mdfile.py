from pathlib import Path
import os
import pypandoc
import settings
from rich import console

console = console.Console()


class MdFile:

    async def data(self):
        """

        :return: list of notes
        """
        data = []
        p = Path(settings.FOLDER).glob('**/*.md')
        for full_file in p:
            file = os.path.basename(str(full_file))
            with open(str(full_file)) as md_file:
                content = md_file.read()

                content = pypandoc.convert_text(source=content,
                                                to='html',
                                                format=settings.PYPANDOC_MARKDOWN)
                data.append({'title': file, 'body': content})
        return data
