from admin_app.db_service import DbService


class UserActiveRecord:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.is_admin = False
        self.created = None
        self.is_deleted = False

    # TODO не обрабатываю вообще ничего
    def save(self):
        sql = 'INSERT INTO User(username, password, is_admin) VALUES (%s, %s, %s)'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.username, self.password, self.is_admin))

    def delete(self):
        if self.id is None:
            return
        sql = 'UPDATE User SET is_deleted = TRUE WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.id,))
            self.is_deleted = True

    def restore(self):
        if self.id is None:
            return
        sql = 'UPDATE User SET is_deleted = FALSE WHERE id = %s'
        with DbService.get_connection() as cursor:
            cursor.execute(sql, (self.id,))
            self.is_deleted = False

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
        self.author_id = None
        self.created = None
        self.is_deleted = False

    def save(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class UserGroupActiveRecord:
    def __init__(self):
        self.user_id = None
        self.group_id = None
        self.permission = None
