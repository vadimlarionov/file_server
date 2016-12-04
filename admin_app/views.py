import uuid
from collections import namedtuple

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


# @login_required
# @admin_required  # хватит и одного, но двойной декоратор это круто
def add_user(request):
    form = AddUserForm(request.POST or None)
    try:
        if form.is_valid():
            user = UserLogic.create_user(form.cleaned_data)
            messages.success(request, 'Пользователь {} создан. Его id = {}'.format(user.username, user.id))
            return redirect('/admin/users/add')
    except exceptions.UserExistException:
        messages.warning(request, 'Такой пользователь уже существует')
    except Exception as e:
        messages.warning(request, e)
    return render(request, 'admin/user_add.html', {'form': form})


@login_required
@admin_required
def add_group(request):
    form = AddGroupForm(request.POST or None)
    try:
        if form.is_valid():
            group = GroupLogic.create_group(form.cleaned_data)
            if group is not None:
                messages.success(request, 'Группа "{}" была создана. Её id = {}'.format(group.title, group.id))
            return redirect('/admin/groups/add')
    except exceptions.UserExistException:
        messages.warning(request, 'Такой пользователь уже существует')
    except Exception as e:
        messages.warning(request, e)
    return render(request, 'admin/group_add.html', {'form': form})


@login_required
@admin_required
def search_user(request):
    form = SearchUserForm(request.GET or None)
    users = []
    if form.is_valid():
        users = UserLogic.get_users(form.cleaned_data['query'])
    return render(request, 'admin/search.html', {'users': users})


@login_required
@admin_required
def user_groups_list(request, user_id):
    u = None
    user_groups = None
    other_groups = None
    try:
        u = UserLogic.get_user_by_id(user_id)
        user_groups = GroupActiveRecord.get_user_groups(user_id)
        sorted(user_groups, key=lambda group: group.id)
        other_groups = GroupActiveRecord.get_groups_without_user(user_id)
        sorted(other_groups, key=lambda group: group.id)
    except Exception as e:
        messages.warning(request, e)

    UserGroupsWithDeleteForm = namedtuple('UserGroupsWithDeleteForm', ['group', 'form'])
    user_groups_with_delete_forms = [UserGroupsWithDeleteForm(group, UserGroupForm({
        'group_id': group.id, 'user_id': u.id})) for group in user_groups]

    GroupsWithoutUserWithForm = namedtuple('GroupsWithoutUserWithForm', ['group', 'form'])
    groups_without_user_with_forms = [
        GroupsWithoutUserWithForm(group, UserGroupForm({'user_id': u.id, 'group_id': group.id}))
        for group in other_groups]

    context = {'u': u, 'user_groups': user_groups_with_delete_forms, 'other_groups': groups_without_user_with_forms}
    return render(request, 'admin/user_groups.html', context)


@login_required
@admin_required
def add_user_to_group(request):
    """Добавить пользователя в группу"""
    form = UserGroupForm(request.POST)
    if form.is_valid():
        try:
            UserGroupActiveRecord.add_user_to_group(form.cleaned_data['user_id'], form.cleaned_data['group_id'])
        except Exception as e:
            messages.warning(request, e)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@admin_required
def delete_user_from_group(request):
    """Удалить пользователя из группы"""
    form = UserGroupForm(request.POST)
    if form.is_valid():
        UserGroupActiveRecord.delete_user_from_group(form.cleaned_data['user_id'], form.cleaned_data['group_id'])
    return redirect(request.META.get('HTTP_REFERER', '/'))
