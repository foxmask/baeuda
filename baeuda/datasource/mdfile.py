# coding: utf-8
from pathlib import Path
import pypandoc
import settings
from rich import console

console = console.Console()


class MdFile:

    async def get_data(self, my_file):
        with open(str(my_file)) as md_file:
            content = md_file.read()
            return pypandoc.convert_text(source=content,
                                         to='html',
                                         format=settings.PYPANDOC_MARKDOWN)

    async def data(self, my_file=''):
        """

        :return: list of notes
        """
        data = []
        if my_file:
            data.append({'body': await self.get_data(my_file)})
        else:
            p = Path(settings.FOLDER).glob('*.md')
            for full_file in p:
                data.append({'body': await self.get_data(full_file)})

        return data
