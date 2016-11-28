from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=70, min_length=4)
    password = forms.CharField(max_length=50, min_length=3)


class AddUserForm(forms.Form):
    username = forms.CharField(max_length=70, min_length=4)
    password = forms.CharField(max_length=50, min_length=3)
    is_admin = forms.BooleanField(required=False)
