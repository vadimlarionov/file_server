from admin_app.data_access_layer.active_records import *
from admin_app.data_access_layer import exceptions


class UserLogic:
    @staticmethod
    def create_user(cleaned_data):
        user = UserActiveRecord.get_by_username(cleaned_data['username'])
        if user is not None:
            raise exceptions.UserExistException

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


class GroupLogic:
    @staticmethod
    def create_group(cleaned_data):
        if not cleaned_data['title']:
            print('title is None or empty')
            return None
        group = GroupActiveRecord()
        group.title = cleaned_data['title']
        group.is_deleted = False
        group.create()
        return group

    @staticmethod
    def delete_group(identity):
        group = GroupActiveRecord.get_by_identity(identity)
        if group is None:
            raise exceptions.NotFoundException
        group.delete()
        return group


class SessionLogic:
    @staticmethod
    def create_session(username, session_key):
        session = SessionActiveRecord()
        session.session_key = str(session_key)
        session.user_id = int(UserActiveRecord.find(username)[0].id)
        session.expire_date = None  # TODO
        session.create()
        return session

    @staticmethod
    def delete_session(session_key):
        session = SessionActiveRecord.get_by_identity(session_key)
        if session is None:
            raise exceptions.NotFoundException
        session.delete()


class UserGroups:
    @staticmethod
    def get_user_groups(user_id):
        if int(user_id) <= 0:
            return


        return UserGroupActiveRecord.get_user_groups(user_id)

    @staticmethod
    def get_other_groups(user_id):
        """Вернуть группы, в который не состоит пользователь"""
        pass
