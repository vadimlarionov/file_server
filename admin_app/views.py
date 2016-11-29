from django.contrib import messages
from django.shortcuts import render, redirect

from admin_app.business_logic_layer.logic import *
from admin_app.data_access_layer import exceptions
from admin_app.forms import *
from auth_utils import login_required


@login_required
def index(request):
    print('index view')
    return render(request, 'index.html')


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
            user = UserLogic.create_user(form.cleaned_data)
            messages.success(request, 'Пользователь {} создан. Его id = {}'.format(user.username, user.id))
            return redirect('/admin/users/add')
    except exceptions.UserExistException:
        messages.warning(request, 'Такой пользователь уже существует')
    except Exception as e:
        messages.warning(request, e)
    return render(request, 'user_add.html', {'form': form})


def add_group(request):
    form = AddGroupForm(request.POST or None)
    try:
        if request.method == 'POST' and form.is_valid():
            group = GroupLogic.create_group(form.cleaned_data)
            if group is not None:
                messages.success(request, 'Группа "{}" была создана. Её id = {}'.format(group.title, group.id))
            return redirect('/admin/groups/add')
    except exceptions.UserExistException:
        messages.warning(request, 'Такой пользователь уже существует')
    except Exception as e:
        messages.warning(request, e)
    return render(request, 'group_add.html', {'form': form})


def search_user(request):
    form = SearchUserForm(request.GET or None)
    users = []
    if form.is_valid():
        users = UserLogic.get_users(form.cleaned_data['query'])
    print(users)ч
    return render(request, 'search.html', {'users': users})
