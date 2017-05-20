from admin_app.db_service import DbService


class Catalogue:
    @staticmethod
    def get_by_id(catalogue_id):
        return CatalogueActiveRecord.get_by_id(catalogue_id)


class CatalogueActiveRecord:
    def __init__(self):
        self.id = None
        self.title = None
        self.author_id = None

    @staticmethod
    def get_by_group_id(group_id):
        """Вернуть каталоги, которые доступны группе"""
        sql = 'SELECT * FROM Catalogue INNER JOIN GroupsCatalogue ' \
              'ON Catalogue.id = GroupsCatalogue.catalogue_id WHERE group_id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (group_id,))
            rows = cursor.fetchall()
        if rows:
            return [CatalogueActiveRecord.__deserialize__(row) for row in rows]
        return []

    @staticmethod
    def get_catalogues_without_group(group_id):
        sql = 'SELECT * FROM Catalogue WHERE id NOT IN (SELECT catalogue_id FROM GroupsCatalogue WHERE group_id = %s)'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (group_id,))
            rows = cursor.fetchall()
        if rows:
            return [CatalogueActiveRecord.__deserialize__(row) for row in rows]
        return []

    @staticmethod
    def get_by_id(catalogue_id):
        sql = 'SELECT * FROM Catalogue WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (catalogue_id,))
            return CatalogueActiveRecord.__deserialize__(cursor.fetchone())

    @staticmethod
    def __deserialize__(row):
        if row is None:
            return None
        catalogue = CatalogueActiveRecord()
        catalogue.id = int(row['id'])
        catalogue.title = str(row['title'])
        catalogue.author_id = row['author_id']
        return catalogue
