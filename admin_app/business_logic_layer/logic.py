import uuid

from admin_app.data_access_layer.active_records import *


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
        return GroupActiveRecord.get_user_groups(user_id)

    @staticmethod
    def get_other_groups(user_id):
        """Вернуть группы, которым не принадлежит пользователь"""
        if int(user_id) <= 0:
            return []
        return GroupActiveRecord.get_groups_without_user(user_id)


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
            raise exceptions.NotFoundException
        session.delete()


class Group:
    @staticmethod
    def create(title):
        if not title:
            print('title is None or empty')
            raise ValueError
        group = GroupActiveRecord()
        group.title = str(title)
        group.is_deleted = False
        group.create()
        return group

    @staticmethod
    def delete_group(identity):
        group = GroupActiveRecord.get_by_id(identity)
        if group is None:
            raise exceptions.NotFoundException
        group.delete()
        return group

    @staticmethod
    def get_groups(title_like):
        if not title_like:
            return []
        return GroupActiveRecord.find(title_like)

    @staticmethod
    def add_catalogue(group_id, catalogue_id, permission):
        group_id = int(group_id)
        catalogue_id = int(catalogue_id)
        permission = int(permission)
        if any([group_id <= 0, catalogue_id <= 0, permission <= 0, permission > 3]):
            raise ValueError()

        group = Group.get_by_id(group_id)
        if not group:
            print('Group not found')
            return None

        catalogue = Catalogue.get_by_id(catalogue_id)
        if not catalogue:
            print('Catalogue not found')
            return None

        group_catalogue = GroupsCatalogueActiveRecord()
        group_catalogue.group_id = group_id
        group_catalogue.catalogue_id = catalogue_id
        group_catalogue.permission = permission
        group_catalogue.create()
        return group_catalogue

    @staticmethod
    def update_permission_in_catalogue(group_id, catalogue_id, permission):
        group_id = int(group_id)
        catalogue_id = int(catalogue_id)
        permission = int(permission)
        if any([group_id <= 0, catalogue_id <= 0, permission <= 0, permission > 3]):
            raise ValueError()
        group_catalogue = GroupsCatalogueActiveRecord()
        group_catalogue.group_id = group_id
        group_catalogue.catalogue_id = catalogue_id
        group_catalogue.permission = permission
        group_catalogue.update_permission()
        return group_catalogue

    @staticmethod
    def delete_catalogue(group_id, catalogue_id):
        """Удаляет каталог из группы"""
        group_id = int(group_id)
        catalogue_id = int(catalogue_id)
        if any([group_id <= 0, catalogue_id <= 0]):
            raise ValueError()
        group_catalogue = GroupsCatalogueActiveRecord()
        group_catalogue.group_id = group_id
        group_catalogue.catalogue_id = catalogue_id
        group_catalogue.delete()

    @staticmethod
    def get_by_id(group_id):
        if int(group_id) <= 0:
            raise ValueError
        return GroupActiveRecord.get_by_id(group_id)

    @staticmethod
    def get_catalogues_without_group(group_id):
        if int(group_id) <= 0:
            raise ValueError
        return CatalogueActiveRecord.get_catalogues_without_group(group_id)

    @staticmethod
    def delete_user(user_id, group_id):
        """Удалить пользователя из группы"""
        user_id = int(user_id)
        group_id = int(group_id)
        if any([user_id <= 0, group_id <= 0]):
            return None
        UserGroupActiveRecord.delete_user_from_group(user_id, group_id)

    @staticmethod
    def add_user(user_id, group_id):
        return UserGroupActiveRecord.add_user_to_group(user_id, group_id)


class Catalogue:
    @staticmethod
    def get_groups(group_id):
        if int(group_id) <= 0:
            raise ValueError
        return GroupCatalogue.get_by_group_id(group_id)

    @staticmethod
    def get_by_id(catalogue_id):
        return CatalogueActiveRecord.get_by_id(catalogue_id)
