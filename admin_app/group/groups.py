from admin_app.catalogue.catalogue import CatalogueActiveRecord, Catalogue
from admin_app.db_service import DbService
from admin_app.exceptions.exceptions import NotFoundException


class Group:
    @staticmethod
    def create(title):
        if not title:
            print('title is None or empty')
            raise ValueError
        group = GroupActiveRecord()
        group.title = str(title)
        group.is_deleted = False
        group.create()
        return group

    @staticmethod
    def delete_group(identity):
        group = GroupActiveRecord.get_by_id(identity)
        if group is None:
            raise NotFoundException()
        group.delete()
        return group

    @staticmethod
    def get_groups(title_like):
        if not title_like:
            return []
        return GroupActiveRecord.find(title_like)

    @staticmethod
    def add_catalogue(group_id, catalogue_id, permission):
        group_id = int(group_id)
        catalogue_id = int(catalogue_id)
        permission = int(permission)
        if any([group_id <= 0, catalogue_id <= 0, permission <= 0, permission > 3]):
            raise ValueError()

        group = Group.get_by_id(group_id)
        if not group:
            print('Group not found')
            return None

        catalogue = Catalogue.get_by_id(catalogue_id)
        if not catalogue:
            print('Catalogue not found')
            return None

        return GroupCatalogue.add_catalogue_to_group(group, catalogue, permission)

    @staticmethod
    def update_permission_in_catalogue(group_id, catalogue_id, permission):
        GroupCatalogue.update_permission_in_catalogue(group_id, catalogue_id, permission)

    @staticmethod
    def delete_catalogue(group_id, catalogue_id):
        """Удаляет каталог из группы"""
        GroupCatalogue.delete_catalogue_from_group(group_id, catalogue_id)

    @staticmethod
    def get_by_id(group_id):
        if int(group_id) <= 0:
            raise ValueError
        return GroupActiveRecord.get_by_id(group_id)

    @staticmethod
    def get_catalogues(group_id):
        if int(group_id) <= 0:
            raise ValueError
        return GroupCatalogue.get_by_group_id(group_id)

    @staticmethod
    def get_catalogues_without_group(group_id):
        if int(group_id) <= 0:
            raise ValueError
        return CatalogueActiveRecord.get_catalogues_without_group(group_id)

    @staticmethod
    def delete_user(user_id, group_id):
        """Удалить пользователя из группы"""
        user_id = int(user_id)
        group_id = int(group_id)
        if any([user_id <= 0, group_id <= 0]):
            return None
        UserGroupActiveRecord.delete_user_from_group(user_id, group_id)

    @staticmethod
    def add_user(user_id, group_id):
        return UserGroupActiveRecord.add_user_to_group(user_id, group_id)

    @staticmethod
    def get_user_groups(user_id):
        return GroupActiveRecord.get_user_groups(user_id)

    @staticmethod
    def get_groups_without_user(user_id):
        """Вернуть группы, которым не принадлежит пользователь"""
        if int(user_id) <= 0:
            return []
        return GroupActiveRecord.get_groups_without_user(user_id)


class GroupActiveRecord:
    def __init__(self):
        self.id = None
        self.title = None
        self.created = None
        self.is_deleted = False

    def create(self):
        sql = 'INSERT INTO Groups(title) VALUES (%s)'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.title,))
            self.id = cursor.lastrowid
        if self.id is not None:
            return GroupActiveRecord.get_by_id(self.id)

    def save(self):
        sql = 'UPDATE Groups SET title = %s, self.is_delete = %s WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.title, self.is_deleted, self.id))

    def delete(self):
        sql = 'UPDATE Groups SET is_deleted = 1 WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql)
            self.is_deleted = True

    @staticmethod
    def get_by_id(identity):
        sql = 'SELECT * FROM Groups WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (int(identity),))
            return GroupActiveRecord.deserialize(cursor.fetchone())

    @staticmethod
    def get_user_groups(user_id):
        """Вернуть группы, в которых состоит пользователь"""
        sql = 'SELECT * FROM Groups INNER JOIN UserGroup ON Groups.id = UserGroup.group_id WHERE user_id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
        if rows:
            return [GroupActiveRecord.deserialize(row) for row in rows]
        return []

    @staticmethod
    def get_groups_without_user(user_id):
        """Вернуть группы, в которых не состоит пользователь"""
        # Да простит меня Павел
        sql = 'SELECT * FROM Groups WHERE id NOT IN ' \
              '(SELECT id FROM Groups INNER JOIN UserGroup ON Groups.id = UserGroup.group_id WHERE user_id = %s);'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
        if rows:
            return [GroupActiveRecord.deserialize(row) for row in rows]
        return []

    @staticmethod
    def find(title_like):
        if not title_like:
            return None
        title_like += '%'
        sql = 'SELECT * FROM Groups WHERE title LIKE %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (title_like,))
            rows = cursor.fetchall()
        if rows:
            return [GroupActiveRecord.deserialize(row) for row in rows]
        return []

    @staticmethod
    def deserialize(row):
        if row is None:
            return None
        group = GroupActiveRecord()
        group.id = int(row['id'])
        group.title = str(row['title'])
        group.created = row['created']
        group.is_deleted = bool(row['is_deleted'])
        return group


class UserGroupActiveRecord:
    def __init__(self):
        self.user_id = None
        self.group_id = None

    @staticmethod
    def delete_user_from_group(user_id, group_id):
        """Удалить пользователя из группы"""
        sql = 'DELETE FROM UserGroup WHERE user_id = %s AND group_id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (user_id, group_id))

    @staticmethod
    def add_user_to_group(user_id, group_id):
        sql = 'INSERT INTO UserGroup(user_id, group_id) VALUES (%s, %s)'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (user_id, group_id))

    def __str__(self):
        return 'UserGroup: user_id={}, groupId={}'.format(self.user_id, self.group_id)


class GroupCatalogue:
    def __init__(self):
        self.group = None
        self.catalogue = None
        self.permission = None

    @staticmethod
    def get_by_group_id(group_id):
        sql = 'SELECT * FROM Groups INNER JOIN GroupsCatalogue ON Groups.id = GroupsCatalogue.group_id ' \
              'INNER JOIN Catalogue ON GroupsCatalogue.catalogue_id = Catalogue.id WHERE group_id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (group_id,))
            rows = cursor.fetchall()
        if rows:
            return [GroupCatalogue.__deserialize__(row) for row in rows]
        return []

    @staticmethod
    def add_catalogue_to_group(group, catalogue, permission):
        group_catalogue = GroupsCatalogueActiveRecord()
        group_catalogue.group_id = group.id
        group_catalogue.catalogue_id = catalogue.id
        group_catalogue.permission = permission
        group_catalogue.create()
        return group_catalogue

    @staticmethod
    def update_permission_in_catalogue(group_id, catalogue_id, permission):
        group_id = int(group_id)
        catalogue_id = int(catalogue_id)
        permission = int(permission)
        if any([group_id <= 0, catalogue_id <= 0, permission <= 0, permission > 3]):
            raise ValueError()
        group_catalogue = GroupsCatalogueActiveRecord()
        group_catalogue.group_id = group_id
        group_catalogue.catalogue_id = catalogue_id
        group_catalogue.permission = permission
        group_catalogue.update_permission()
        return group_catalogue

    @staticmethod
    def delete_catalogue_from_group(group_id, catalogue_id):
        """Удаляет каталог из группы"""
        group_id = int(group_id)
        catalogue_id = int(catalogue_id)
        if any([group_id <= 0, catalogue_id <= 0]):
            raise ValueError()
        group_catalogue = GroupsCatalogueActiveRecord()
        group_catalogue.group_id = group_id
        group_catalogue.catalogue_id = catalogue_id
        group_catalogue.delete()

    @staticmethod
    def __deserialize__(row):
        if row is None:
            return None
        group = GroupActiveRecord()
        group.id = row['group_id']
        group.created = row['created']
        group.title = row['title']
        group.is_deleted = row['is_deleted']

        catalogue = CatalogueActiveRecord()
        catalogue.id = row['catalogue_id']
        catalogue.title = row['Catalogue.title']
        catalogue.author_id = row['author_id']

        group_catalogue = GroupCatalogue()
        group_catalogue.group = group
        group_catalogue.catalogue = catalogue
        group_catalogue.permission = row['permission']
        return group_catalogue


class GroupsCatalogueActiveRecord:
    def __init__(self):
        self.group_id = None
        self.catalogue_id = None
        self.permission = None

    def create(self):
        sql = 'INSERT INTO GroupsCatalogue(group_id, catalogue_id, permission) VALUES (%s, %s, %s)'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.group_id, self.catalogue_id, self.permission))

    def update_permission(self):
        sql = 'UPDATE GroupsCatalogue SET permission = %s WHERE group_id = %s AND catalogue_id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.permission, self.group_id, self.catalogue_id))

    def delete(self):
        sql = 'DELETE FROM GroupsCatalogue WHERE group_id = %s AND catalogue_id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.group_id, self.catalogue_id))