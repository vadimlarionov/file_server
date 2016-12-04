from django import forms

from admin_app.data_access_layer.active_records import UserActiveRecord


class LoginForm(forms.Form):
    username = forms.CharField(max_length=70, min_length=4, label='Имя пользователя')
    password = forms.CharField(max_length=50, min_length=3, label='Пароль')

    def is_valid(self):
        if not super().is_valid():
            return False
        try:
            user = UserActiveRecord.get_by_username(self.cleaned_data['username'])
        except KeyError:
            return False
        if not user:
            return False
        return user.password == self.cleaned_data['password']


class AddUserForm(forms.Form):
    username = forms.CharField(max_length=70, min_length=4, label='Имя пользователя')
    password = forms.CharField(max_length=50, min_length=3, label='Пароль')
    is_admin = forms.BooleanField(required=False, label='Это администратор')


class AddGroupForm(forms.Form):
    title = forms.CharField(max_length=256, min_length=1, label='Заголовок')


class SearchForm(forms.Form):
    query = forms.CharField(max_length=256, min_length=1)


class AddUserToGroupForm(forms.Form):
    user_id = forms.IntegerField(min_value=1)
    group_id = forms.IntegerField(min_value=1)
    permission = forms.IntegerField(min_value=1, max_value=3)


class UserGroupForm(forms.Form):
    user_id = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
    group_id = forms.IntegerField(min_value=1, widget=forms.HiddenInput)


class GroupCatalogueForm(forms.Form):
    group_id = forms.IntegerField(min_value=1)
    catalogue_id = forms.IntegerField(min_value=1)
    permission = forms.IntegerField(min_value=1, max_value=3)
    action = forms.CharField(required=False)
