from django.shortcuts import render, redirect

from admin_app.forms import *
from auth_utils import login_required
from django.contrib import messages
from admin_app.data_access_layer.active_records import *


@login_required
def index(request):
    print('index view')
    return render(request, 'index.html')


def base(request):
    return render(request, 'base.html')


def login(request):
    print('login view')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('Form is valid')
        else:
            print('Form is not valid')
    else:
        return index(request)

    response = redirect('/')
    response.set_cookie('foo', 'bar')
    return response


def add_user(request):
    form = AddUserForm(request.POST or None)
    try:
        if request.method == 'POST' and form.is_valid():
            user = UserActiveRecord()
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password']
            user.is_admin = bool(form.cleaned_data['is_admin'])
            user.save()
            messages.success(request, 'Пользователь {} создан'.format(form.cleaned_data['username']))
    except Exception as e:
        messages.warning(request, e)
    messages.success(request, 'yee')
    return render(request, 'add_user.html', {'form': form})
