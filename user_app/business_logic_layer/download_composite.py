import os
from abc import abstractmethod

import zipfile

from file_server.settings import MEDIA_DIR


class DownloadableComponent:
    @abstractmethod
    def download(self):
        """
        Скачать компонент.
        """
        pass


class DownloadableFile(DownloadableComponent):
    def __init__(self, file):
        self.file = file

    def download(self):
        """
        Скачать файл.
        """
        path = os.path.join(MEDIA_DIR, str(self.file.path))
        return path


class DownloadableCatalog(DownloadableComponent):
    def __init__(self, ):
        self.files = []

    def add(self, file):
        self.files.append(file)

    def download(self):
        """
        Сформировать zip-архив с файлами.
        """
        paths = [f.file.path
                 for f in self.files]

        zipfile_path = 'catalog.zip'

        zipf = zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED)
        for path in paths:
            zipf.write(
                os.path.join(MEDIA_DIR, str(path)), path
            )

        zipf.close()

        return zipfile_path
