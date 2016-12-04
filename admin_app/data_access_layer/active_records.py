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
        """
        Добавляет пользователя в БД
        """
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
        """
        Обновляет информацию о пользователе
        """
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
    def get_by_identity(identity):
        try:
            identity = int(identity)
        except ValueError:
            print('identity is not int, identity={}'.format(identity))
            return

        sql = 'SELECT * FROM User WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (identity,))
            row = cursor.fetchone()
            if row is not None:
                print('row: ', row)
                return UserActiveRecord.deserialize(row)
        return None

    @staticmethod
    def find(username_like):
        username_like += '%'
        sql = 'SELECT * FROM User WHERE username LIKE %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (username_like,))
            all_rows = cursor.fetchall()
        users = []
        if all_rows is not None:
            for row in all_rows:
                users.append(UserActiveRecord.deserialize(row))
        return users

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
            return GroupActiveRecord.get_by_identity(self.id)

    def save(self):
        sql = 'UPDATE Groups SET title = %s, self.is_delete = %s WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.title, self.is_deleted, self.id))

    def delete(self):
        if self.id is None:
            print('Group id is None')
            return
        sql = 'UPDATE Groups SET is_deleted = 1 WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql)
            self.is_deleted = True

    @staticmethod
    def get_by_identity(identity):
        sql = 'SELECT * FROM Groups WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (int(identity),))
            return GroupActiveRecord.deserialize(cursor.fetchone())

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
        self.permission = None

    @staticmethod
    def get_user_groups(user_id):
        sql = 'SELECT * FROM Groups INNER JOIN User_group ON Groups.id = User_group.group_id WHERE user_id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (user_id,))
            all_rows = cursor.fetchall()
        groups = []
        if all_rows:
            for row in all_rows:
                groups.append(GroupWithPermission.deserialize(row))
        return groups


class GroupWithPermission:
    def __init__(self):
        self.user_id = None
        self.group_id = None
        self.title = None
        self.group_created = None
        self.group_is_deleted = None
        self.permission = None

    @staticmethod
    def deserialize(row):
        if not row:
            return None
        group_with_permission = GroupWithPermission()
        group_with_permission.user_id = int(row['user_id'])
        group_with_permission.group_id = int(row['group_id'])
        group_with_permission.title = row['title']
        group_with_permission.group_created = row['created']
        group_with_permission.permission = int(row['permission'])
        return group_with_permission
