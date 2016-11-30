from django import forms

from admin_app.data_access_layer.active_records import UserActiveRecord


class LoginForm(forms.Form):
    username = forms.CharField(max_length=70, min_length=4)
    password = forms.CharField(max_length=50, min_length=3)

    def is_valid(self):
        super().is_valid()
        try:
            user = UserActiveRecord.find(self.cleaned_data['username'])[0]  # TODO возвращает список?
        except KeyError:
            return False
        return user.password == self.cleaned_data['password']


class AddUserForm(forms.Form):
    username = forms.CharField(max_length=70, min_length=4)
    password = forms.CharField(max_length=50, min_length=3)
    is_admin = forms.BooleanField(required=False)


class AddGroupForm(forms.Form):
    title = forms.CharField(max_length=256, min_length=1)


class SearchUserForm(forms.Form):
    query = forms.CharField(max_length=256, min_length=1)
