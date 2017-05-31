import os

from user_app.business_logic_layer.download_composite import DownloadableCatalog, DownloadableFile
from user_app.data_access_layer.gateways import CatalogueGateway, FileGateway, GroupCatalogueGateway
from file_server.settings import MEDIA_DIR

PERMISSION_R, PERMISSION_W, PERMISSION_WR = 1, 2, 3


class TransactionScript:
    @staticmethod
    def get_user_catalogues(user_id):
        """
        Получить каталоги, непосредственно созданные пользователем.
        """
        # NB: не возвращает каталоги групп
        if not user_id:
            raise ValueError('Не указан параметр user_id')
        return CatalogueGateway.find_by_user_id(user_id)

    @staticmethod
    def get_shared_catalogues(user_id):
        """
        Получить каталоги групп, к которым принадлежит пользователь.
        """
        if not user_id:
            raise ValueError('Не указан параметр user_id')
        return CatalogueGateway.find_shared_by_user_id(user_id)

    @staticmethod
    def get_catalogue(cat_id):
        """
        Получить каталог по id.
        """
        if not cat_id:
            raise ValueError('Не указан параметр cat_id')
        return CatalogueGateway.find_by_id(cat_id)

    @staticmethod
    def get_permission_on_catalogue(cat_id, user_id):
        """
        Получить доступ к каталогу по id каталога и пользователя.
        """
        if not cat_id:
            raise ValueError('Не указан параметр cat_id')
        if not user_id:
            raise ValueError('Не указан параметр user_id')
        query_result = GroupCatalogueGateway.find_by_cat_id_and_user_id(cat_id, user_id)
        if not query_result:
            return PERMISSION_WR
        else:
            return int(query_result['permission'])

    @staticmethod
    def get_catalogue_files(cat_id):
        """
        Получить список файлов в каталоге.
        """
        if not cat_id:
            raise ValueError('Не указан параметр cat_id')
        return FileGateway.find_by_cat_id(cat_id)

    @staticmethod
    def get_file(file_id):
        """
        Получить файл по id.
        """
        if not file_id:
            raise ValueError('Не указан параметр file_id')
        return FileGateway.find_by_id(file_id)

    @staticmethod
    def create_catalogue(title, user_id):
        """
        Создать каталог.
        """
        if not title:
            raise ValueError('Не указан параметр title')
        if not user_id:
            raise ValueError('Не указан параметр user_id')
        CatalogueGateway.create(title, user_id)

    @staticmethod
    def download_file(file):
        """
        Скачать указанный файл (загрузить в хранилище).
        """
        if not file:
            raise ValueError('Не указан параметр file')
        with open(os.path.join(MEDIA_DIR, str(file)), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    @staticmethod
    def download_catalogue(cat_id):
        """
        Скачать указанный каталог.
        """

        files = FileGateway.find_by_cat_id(cat_id)

        print(files)

        downloadable_files = [DownloadableFile(f) for f in files]
        catalog_composite = DownloadableCatalog()

        for f in downloadable_files:
            catalog_composite.add(f)

        data = catalog_composite.download()

        return data


    @staticmethod
    def save_file(file_data, user_id, cat_id):
        """
        Создать запись об указанном файле.
        """
        if not file_data:
            raise ValueError('Не указан параметр file_data')
        if not user_id:
            raise ValueError('Не указан параметр user_id')
        if not cat_id:
            raise ValueError('Не указан параметр cat_id')
        file = file_data['file']
        TransactionScript.download_file(file)
        FileGateway.create(file_data, user_id, cat_id)

    @staticmethod
    def delete_file(file_id):
        """
        Удалить указанный файл.
        """
        if not file_id:
            raise ValueError('Не указан параметр file_id')
        file = TransactionScript.get_file(file_id)
        os.remove(os.path.join(MEDIA_DIR, file.path))
        FileGateway.delete_by_id(file_id)

    @staticmethod
    def edit_file(file_id, file_data):
        """
        Редактировать указанный файл.
        """
        if not file_id:
            raise ValueError('Не указан параметр file_id')

        FileGateway.update(file_data, file_id)

    @staticmethod
    def delete_catalogue(catalogue_id):
        """
        Удалить указанный каталог и входящие в него файлы.
        """
        if not catalogue_id:
            raise ValueError('Не указан catalogue_id')
        files = TransactionScript.get_catalogue_files(catalogue_id)
        for file in files:
            TransactionScript.delete_file(file.id)
        CatalogueGateway.delete_by_id(catalogue_id)
