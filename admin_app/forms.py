from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=70, min_length=4)
    password = forms.CharField(max_length=50, min_length=3)


class AddUserForm(forms.Form):
    username = forms.CharField(max_length=70, min_length=4)
    password = forms.CharField(max_length=50, min_length=3)
    is_admin = forms.BooleanField(required=False)


class AddGroupForm(forms.Form):
    title = forms.CharField(max_length=256, min_length=1)


class SearchUserForm(forms.Form):
    query = forms.CharField(max_length=256, min_length=1)
