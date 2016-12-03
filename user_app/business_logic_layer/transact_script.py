import os

from user_app.data_access_layer.gateways import CatalogueGateway, FileGateway
from file_server.settings import MEDIA_DIR


class TransactionScript:
    @staticmethod
    def get_user_catalogues(user_id):
        return CatalogueGateway.find_by_user_id(user_id)

    @staticmethod
    def get_catalogue(cat_id):
        return CatalogueGateway.find_by_id(cat_id)

    @staticmethod
    def get_catalogue_files(cat_id):
        return FileGateway.find_by_cat_id(cat_id)

    @staticmethod
    def get_file(file_id):
        return FileGateway.find_by_id(file_id)

    @staticmethod
    def create_catalogue(title, user_id):
        CatalogueGateway.create(title, user_id)

    @staticmethod
    def download_file(file):
        with open(os.path.join(MEDIA_DIR, str(file)), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    @staticmethod
    def save_file(file_data, user_id, cat_id):
        file = file_data['file']
        TransactionScript.download_file(file)
        FileGateway.create(file_data, user_id, cat_id)

    @staticmethod
    def delete_file():
        pass

    @staticmethod
    def delete_catalog():
        pass

