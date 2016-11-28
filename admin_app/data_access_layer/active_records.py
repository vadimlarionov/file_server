from admin_app.db_service import DbService
from pymysql.err import MySQLError
from admin_app.data_access_layer import exceptions
from admin_app.data_access_layer import constants


class UserActiveRecord:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.is_admin = False
        self.created = None
        self.is_deleted = False

    def save(self):
        sql = 'INSERT INTO User(username, password, is_admin) VALUES (%s, %s, %s)'
        try:
            with DbService.get_connection() as cursor:
                cursor.execute(sql, (self.username, self.password, self.is_admin))
                self.id = cursor.lastrowid
        except MySQLError as e:
            if e.args[0] == constants.DUPLICATE_ENTRY:
                raise exceptions.UserExistException
            raise e

    def delete(self):
        if self.id is None:
            return
        try:
            int(self.id)
        except ValueError:
            print('user id is not int')
            return
        sql = 'UPDATE User SET is_deleted = TRUE WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.id,))
            self.is_deleted = True

    def restore(self):
        if self.id is None:
            print("user id is None")
            return
        sql = 'UPDATE User SET is_deleted = FALSE WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.id,))
            self.is_deleted = False

    @staticmethod
    def get_user(username):
        sql = 'SELECT * FROM User WHERE username = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (username, ))
            return UserActiveRecord.__deserialize__(cursor.fetchone())

    @staticmethod
    def find(identity):
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
                print(row)
                return UserActiveRecord.__deserialize__(row)
        return None

    @staticmethod
    def __deserialize__(row):
        if row is None:
            return None
        user = UserActiveRecord()
        user.id = row['id']
        user.username = row['username']
        user.password = row['password']
        user.is_admin = row['is_admin']
        user.created = row['created']
        user.is_deleted = row['is_deleted']
        return user


class SessionActiveRecord:
    def __init__(self):
        self.session_key = None
        self.user_id = None
        self.expire_date = None

    def save(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def get_session(session_key):
        sql = 'SELECT * FROM Session WHERE session_key = %s'
        pass

    @staticmethod
    def __deserialize__(row):
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

    def save(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def create_group(title):
        sql = 'INSERT INTO Groups(title) VALUES (%s)'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, title)
            identity = cursor.lastrowid
        if identity is not None:
            return GroupActiveRecord.find(identity)

    @staticmethod
    def find(identity):
        sql = 'SELECT * FROM Groups WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (int(identity),))

            return GroupActiveRecord.__deserializer__(cursor.fetchone())

    @staticmethod
    def __deserializer__(row):
        if row is None:
            return None
        group = GroupActiveRecord()
        group.id = row['id']
        group.title = row['title']
        group.created = row['created']
        group.is_deleted = row['is_deleted']
        return group


class UserGroupActiveRecord:
    def __init__(self):
        self.user_id = None
        self.group_id = None
        self.permission = None
