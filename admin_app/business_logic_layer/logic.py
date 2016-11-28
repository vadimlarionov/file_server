from admin_app.data_access_layer.active_records import *
from admin_app.data_access_layer import exceptions


class UserLogic:
    @staticmethod
    def create_user(cleaned_data):
        user = UserActiveRecord.get_user(cleaned_data['username'])
        if user is not None:
            raise exceptions.UserExistException

        user = UserActiveRecord()
        user.username = str(cleaned_data['username'])
        user.password = str(cleaned_data['password'])
        user.is_admin = bool(cleaned_data['is_admin'])
        user.save()
        return user


class GroupLogic:
    @staticmethod
    def create_group(cleaned_data):
        if not cleaned_data['title']:
            print('title is None or empty')
            return None
        return GroupActiveRecord.create_group(cleaned_data['title'])
