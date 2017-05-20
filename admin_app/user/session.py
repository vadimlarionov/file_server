import uuid

from admin_app.db_service import DbService
from admin_app.exceptions.exceptions import NotFoundException


class Session:
    @staticmethod
    def create_session(user_id):
        session = SessionActiveRecord()
        session.session_key = str(uuid.uuid4())
        session.user_id = int(user_id)
        session.expire_date = None  # TODO
        session.create()
        return session

    @staticmethod
    def delete_session(session_key):
        session = SessionActiveRecord.get_by_identity(session_key)
        if session is None:
            raise NotFoundException()
        session.delete()


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
