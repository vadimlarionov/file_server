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
    def find_shared_by_user_id(user_id):
        """Найти каталоги по id пользователя."""
        sql = 'SELECT * FROM Catalogue c ' \
              'JOIN GroupsCatalogue gc ON c.id = gc.catalogue_id ' \
              'JOIN Groups g ON gc.group_id = g.id ' \
              'JOIN UserGroup ug ON g.id = ug.group_id ' \
              'JOIN User u ON ug.user_id = u.id ' \
              'WHERE u.id = %s AND author_id != %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (user_id, user_id))
            all_rows = cursor.fetchall()
        catalogs = []
        if all_rows is not None:
            for row in all_rows:
                catalogs.append(CatalogueGateway.__deserialize__(row))
        return catalogs

    @staticmethod
    def get_permission_by_id_and_user_id(cat_id, user_id):
        """Найти доступ к каталогу по id пользователя и каталога."""
        sql = 'SELECT DISTINCT gc.permission FROM Catalogue c ' \
              'JOIN GroupsCatalogue gc ON c.id = gc.catalogue_id ' \
              'JOIN Groups g ON gc.group_id = g.id ' \
              'JOIN UserGroup ug ON g.id = ug.group_id ' \
              'JOIN User u ON ug.user_id = u.id ' \
              'WHERE u.id = %s AND c.id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (user_id, cat_id))
            return int(cursor.fetchone()['permission'])

    @staticmethod
    def delete_by_id(cat_id):
        """Удалить каталог по id."""
        sql = 'UPDATE Catalogue SET author_id = NULL WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (cat_id,))


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
    def create(file_data, user_id, cat_id):
        """Добавить новый файл в БД."""
        sql = 'INSERT INTO File(path, title, description, attributes, other_attributes, user_id, catalogue_id) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s)'
        try:
            with DbService.get_connection() as cursor:
                cursor.execute(sql, (str(file_data['file']), file_data['title'], file_data['description'],
                                     file_data['attributes'], file_data['other_attributes'], user_id, cat_id))
        except MySQLError as e:
            print(e)  # TODO duplicate error?

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
    def find_by_id(file_id):
        """Найти файл по id."""
        sql = 'SELECT * FROM File WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (file_id,))
            row = cursor.fetchone()
        return FileGateway.__deserialize__(row)

    @staticmethod
    def delete_by_id(file_id):
        """Удалить файл по id."""
        sql = 'UPDATE File SET catalogue_id = NULL WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (file_id,))

    @staticmethod
    def __deserialize__(row):
        if row is None:
            return None
        File = namedtuple('File', ['id', 'path', 'description',  'title',
                                   'attributes', 'other_attributes', 'user_id', 'catalogue_id'])
        return File(int(row['id']),
                    str(row['path']),
                    str(row['description']),
                    str(row['title']),
                    str(row['attributes']),
                    str(row['other_attributes']),
                    int(row['user_id']),
                    int(row['catalogue_id']))
