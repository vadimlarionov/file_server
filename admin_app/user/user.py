from admin_app.db_service import DbService
from admin_app.exceptions.exceptions import UserExistException
from admin_app.group.groups import Group
from admin_app.user.session import Session


class User:
    @staticmethod
    def authorize(username):
        """Авторизовывает пользователя. Возвращает сессию"""
        if not username:
            return None
        user = UserActiveRecord.get_by_username(username)
        if not user:
            print('user not found')
            return None
        return Session.create_session(user.id)

    @staticmethod
    def create(cleaned_data):
        user = UserActiveRecord()
        user.username = str(cleaned_data['username'])
        user.password = str(cleaned_data['password'])
        user.is_admin = bool(cleaned_data['is_admin'])
        user.create()
        return user

    @staticmethod
    def get_users(username_like):
        return UserActiveRecord.find(username_like)

    @staticmethod
    def get_user_by_id(user_id):
        user_id = int(user_id)
        if user_id <= 0:
            raise ValueError('user_id must be positive')
        return UserActiveRecord.get_by_id(user_id)

    @staticmethod
    def get_groups(user_id):
        if int(user_id) <= 0:
            return []
        return Group.get_user_groups(user_id)

    @staticmethod
    def get_other_groups(user_id):
        if int(user_id) <= 0:
            return []
        return Group.get_groups_without_user(user_id)


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
            raise UserExistException()

        sql = 'INSERT INTO User(username, password, is_admin) VALUES (%s, %s, %s)'
        try:
            with DbService.get_connection() as cursor:
                cursor.execute(sql, (self.username, self.password, self.is_admin))
                self.id = cursor.lastrowid
        except MySQLError as e:
            if e.args[0] == 1062:  # DUPLICATE_ENTRY
                raise UserExistException()
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
    def get_users():
        sql = 'SELECT * FROM User'
        with DbService.get_connection() as cursor:
            cursor.execute(sql)
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
