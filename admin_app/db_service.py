from pymysql import connect
from pymysql.cursors import DictCursor


class DbService:

    def __init__(self):
        settings_db = {
            'host': 'localhost',
            'user': 'fs_user',
            'password': '8kf5XvcLCqNQ',
            'database': 'fs_db',
            'autocommit': False,
            'cursorclass': DictCursor
        }
        self.connection = connect(**settings_db)

    def execute(self):
        sql = 'SELECT * FROM User'
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
