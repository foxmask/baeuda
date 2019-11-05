from joplin_api import JoplinApi
import pypandoc
import settings


class Joplin:

    def __init__(self):
        self.joplin = JoplinApi(settings.TOKEN)

    def subfolder(self, folder):
        """

        :param folder: subfolder
        :return: line of the founded children
        """
        for line in folder['children']:
            if settings.FOLDER == line['title']:
                return line['id']

    async def folder(self):
        """

        :return: the folder id
        """
        res = await self.joplin.get_folders()
        for line in res.json():
            if settings.FOLDER == line['title']:
                return line['id']
            if 'children' in line:
                folder_id = self.subfolder(line)
                if folder_id is not None:
                    return folder_id

    async def my_folder(self):
        """

        :return: return the folder name used in Joplin
        """
        return settings.FOLDER

    async def data(self):
        """

        :return: list of notes
        """
        data = []
        folder_id = await self.folder()
        notes = await self.joplin.get_folders_notes(folder_id)
        for note in notes.json():
            if settings.FILTER in note['title'] and note['is_todo'] == 0:
                content = pypandoc.convert_text(source=note['body'],
                                                to='html',
                                                format=settings.PYPANDOC_MARKDOWN)
                data.append({'title': note['title'], 'body': content})
        return data
