from admin_app.db_service import DbService


class UserActiveRecord:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.is_admin = False
        self.created = None
        self.is_deleted = False

    def save(self):
        pass

    def delete(self):
        if self.id is None:
            return
        sql = 'UPDATE User SET is_deleted = TRUE WHERE id = %d' % int(self.id)
        with DbService.get_connection() as cursor:
            cursor.execute(sql)
            self.is_deleted = True

    @staticmethod
    def find(identity):
        sql = 'SELECT * FROM User WHERE id = %d' % identity
        with DbService.get_connection() as cursor:
            cursor.execute(sql)
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

    def update(self):
        pass


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
