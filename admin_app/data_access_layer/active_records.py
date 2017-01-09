from pymysql.err import MySQLError

from admin_app.data_access_layer import constants
from admin_app.data_access_layer import exceptions
from admin_app.db_service import DbService


class UserActiveRecord:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.is_admin = False
        self.created = None
        self.is_deleted = False

    def create(self):
        """Добавляет пользователя в БД"""
        user = UserActiveRecord.get_by_username(self.username)
        if user is not None:
            raise exceptions.UserExistException

        sql = 'INSERT INTO User(username, password, is_admin) VALUES (%s, %s, %s)'
        try:
            with DbService.get_connection() as cursor:
                cursor.execute(sql, (self.username, self.password, self.is_admin))
                self.id = cursor.lastrowid
        except MySQLError as e:
            if e.args[0] == constants.DUPLICATE_ENTRY:
                raise exceptions.UserExistException
            raise e

    def save(self):
        """Обновляет информацию о пользователе"""
        sql = 'UPDATE User SET is_admin = %s, is_deleted = %s WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.is_admin, self.is_deleted, self.id))

    def delete(self):
        if self.id is None:
            return
        try:
            int(self.id)
        except ValueError:
            print('user id is not int')
            return
        sql = 'UPDATE User SET is_deleted = 1 WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.id,))
            self.is_deleted = True

    def restore(self):
        if self.id is None:
            print("user id is None")
            return
        sql = 'UPDATE User SET is_deleted = 0 WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.id,))
            self.is_deleted = False

    @staticmethod
    def get_by_username(username):
        sql = 'SELECT * FROM User WHERE username = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (username,))
            return UserActiveRecord.deserialize(cursor.fetchone())

    @staticmethod
    def get_by_id(identity):
        sql = 'SELECT * FROM User WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (identity,))
            row = cursor.fetchone()
            return UserActiveRecord.deserialize(row)

    @staticmethod
    def find(username_like):
        username_like += '%'
        sql = 'SELECT * FROM User WHERE username LIKE %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (username_like,))
            rows = cursor.fetchall()
        if rows:
            return [UserActiveRecord.deserialize(row) for row in rows]
        return []

    @staticmethod
    def deserialize(row):
        if row is None:
            return None
        user = UserActiveRecord()
        user.id = int(row['id'])
        user.username = str(row['username'])
        user.password = str(row['password'])
        user.is_admin = bool(row['is_admin'])
        user.created = row['created']
        user.is_deleted = bool(row['is_deleted'])
        return user

    def __str__(self):
        return 'User: {} {} {}'.format(self.id, self.username, self.is_admin)


class SessionActiveRecord:
    def __init__(self):
        self.id = None
        self.session_key = None
        self.user_id = None
        self.expire_date = None

    def create(self):
        print("Inserting: ", self.session_key, self.user_id, self.expire_date)
        sql = 'INSERT INTO Session(session_key, user_id, expire_date) VALUES (%s, %s, %s)'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.session_key, self.user_id, self.expire_date))
            self.id = cursor.lastrowid
        if self.id is not None:
            return SessionActiveRecord.get_by_identity(self.session_key)

    def delete(self):
        sql = 'UPDATE Session SET user_id = NULL WHERE session_key = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.session_key,))

    @staticmethod
    def get_session(session_key):
        sql = 'SELECT * FROM Session WHERE session_key = %s'

        with DbService.get_connection() as cursor:
            cursor.execute(sql, (session_key,))
            row = cursor.fetchone()
        return SessionActiveRecord.deserialize(row)

    @staticmethod
    def get_by_identity(identity):
        sql = 'SELECT * FROM Session WHERE session_key = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (identity,))
            return SessionActiveRecord.deserialize(cursor.fetchone())

    @staticmethod
    def deserialize(row):
        if not row:
            return None
        session = SessionActiveRecord()
        session.session_key = row['session_key']
        session.user_id = row['user_id']
        session.expire_date = row['expire_date']
        return session


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
        # TODO Да простит меня Павел
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
