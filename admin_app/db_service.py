from pymysql import connect
from pymysql.cursors import DictCursor


class DbService:

    @staticmethod
    def get_connection():
        settings_db = {
            'host': 'localhost',
            'user': 'fs_user',
            'password': '8kf5XvcLCqNQ',
            'database': 'fs_db',
            'autocommit': False,
            'cursorclass': DictCursor
        }
        return connect(**settings_db)
