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
