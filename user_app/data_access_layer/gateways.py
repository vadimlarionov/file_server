from collections import namedtuple

from pymysql import MySQLError

from admin_app.db_service import DbService


class CatalogueGateway:
    """Шлюз таблицы Каталог."""

    @staticmethod
    def create(title, author_id):
        """Добавить новый каталог в БД."""
        sql = 'INSERT INTO Catalogue(title, author_id) VALUES (%s, %s)'
        try:
            with DbService.get_connection() as cursor:
                cursor.execute(sql, (title, author_id))
        except MySQLError as e:
            pass  # TODO duplicate error?

    @staticmethod
    def find_by_id(cat_id):
        """Найти каталог по id."""
        sql = 'SELECT * FROM Catalogue WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (cat_id,))
            row = cursor.fetchone()
        return CatalogueGateway.__deserialize__(row)

    @staticmethod
    def find_by_user_id(user_id):
        """Найти каталоги по id пользователя."""
        sql = 'SELECT * FROM Catalogue WHERE author_id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (user_id,))
            all_rows = cursor.fetchall()
        catalogs = []
        if all_rows is not None:
            for row in all_rows:
                catalogs.append(CatalogueGateway.__deserialize__(row))
        return catalogs

    @staticmethod
    def __deserialize__(row):
        if row is None:
            return None
        Catalogue = namedtuple('Catalogue', ['id', 'title', 'author_id'])
        return Catalogue(int(row['id']),
                         str(row['title']),
                         int(row['author_id']))


class FileGateway:
    """Шлюз таблицы Файл."""

    @staticmethod
    def create(title, user_id, cat_id):
        """Добавить новый файл в БД."""
        sql = 'INSERT INTO File(title, user_id, catalogue_id) VALUES (%s, %s, %s)'
        try:
            with DbService.get_connection() as cursor:
                cursor.execute(sql, (title, user_id, cat_id))
        except MySQLError as e:
            pass  # TODO duplicate error?

    @staticmethod
    def find_by_cat_id(cat_id):
        """Найти файлы по id каталога."""
        sql = 'SELECT * FROM File WHERE catalogue_id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (cat_id,))
            all_rows = cursor.fetchall()
        files = []
        if all_rows is not None:
            for row in all_rows:
                files.append(FileGateway.__deserialize__(row))
        return files

    @staticmethod
    def __deserialize__(row):
        if row is None:
            return None
        File = namedtuple('File', ['id', 'title', 'user_id', 'catalogue_id'])
        return File(int(row['id']),
                    str(row['title']),
                    int(row['user_id']),
                    int(row['catalogue_id']))
