import uuid

from django.contrib import messages
from django.shortcuts import render, redirect

from admin_app.business_logic_layer.logic import *
from admin_app.data_access_layer import exceptions
from admin_app.forms import *
from auth_utils import login_required, admin_required


def index(request):
    return render(request, 'index.html')


def logout(request):
    """Это уязвимость."""
    session_key = request.COOKIES.get('session_key', None)
    SessionLogic.delete_session(session_key)
    return redirect('/')


def login(request):
    print(request.belodedov)
    response = redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            session_key = str(uuid.uuid4())
            SessionLogic.create_session(form.cleaned_data['username'], session_key)
            response.set_cookie('session_key', session_key)
            return response
        else:
            response.set_cookie('session_key', '')
    else:
        return response
    return response


@login_required
@admin_required  # хватит и одного, но двойной декоратор это круто
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


@login_required
@admin_required
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


@login_required
@admin_required
def search_user(request):
    form = SearchUserForm(request.GET or None)
    users = []
    if form.is_valid():
        users = UserLogic.get_users(form.cleaned_data['query'])
    print(users)
    return render(request, 'search.html', {'users': users})
