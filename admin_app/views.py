from collections import namedtuple

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from admin_app.exceptions import exceptions
from admin_app.forms import *
from admin_app.group.groups import Group
from admin_app.reports.reports import ReportFactory, ReportType
from admin_app.user.session import Session
from admin_app.user.user import User
from auth_utils import login_required, admin_required

report_factory = ReportFactory()


def index(request):
    return render(request, 'index.html')


def logout(request):
    """Это уязвимость."""
    session_key = request.COOKIES.get('session_key', None)
    Session.delete_session(session_key)
    return redirect('/')


def login(request):
    print(request.belodedov)
    response = redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            session = User.authorize(form.cleaned_data['username'])
            response.set_cookie('session_key', session.session_key)
            return response
        else:
            response.set_cookie('session_key', '')
    else:
        return response
    return response


@login_required
@admin_required
def add_user(request):
    form = AddUserForm(request.POST or None)
    try:
        if form.is_valid():
            user = User.create(form.cleaned_data)
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
            group = Group.create(form.cleaned_data['title'])
            if group:
                messages.success(request, 'Группа "{}" была создана. Её id = {}'.format(group.title, group.id))
            return redirect('/admin/groups/add')
    except Exception as e:
        messages.warning(request, e)
    return render(request, 'admin/group_add.html', {'form': form})


@login_required
@admin_required
def search(request):
    form = SearchForm(request.GET or None)
    users = []
    groups = []
    if form.is_valid():
        users = User.get_users(form.cleaned_data['query'])
        groups = Group.get_groups(form.cleaned_data['query'])
        if not (users or groups):
            messages.warning(request, 'Не найдено')
    return render(request, 'admin/search.html', {'users': users, 'groups': groups})


@login_required
@admin_required
def user_groups_list(request, user_id):
    u = None
    user_groups = None
    other_groups = None
    try:
        u = User.get_user_by_id(user_id)
        user_groups = User.get_groups(user_id)
        other_groups = User.get_other_groups(user_id)
        sorted(user_groups, key=lambda group: group.id)
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
            Group.add_user(form.cleaned_data['user_id'], form.cleaned_data['group_id'])
        except Exception as e:
            messages.warning(request, e)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@admin_required
def delete_user_from_group(request):
    """Удалить пользователя из группы"""
    form = UserGroupForm(request.POST)
    if form.is_valid():
        Group.delete_user(form.cleaned_data['user_id'], form.cleaned_data['group_id'])
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@admin_required
def group_catalogues(request, group_id):
    """Информация о группе"""
    group = Group.get_by_id(group_id)
    group_catalogues_list = Group.get_catalogues(group_id)
    other_catalogues = Group.get_catalogues_without_group(group_id)

    context = {'g': group, 'g_c_list': group_catalogues_list, 'other_catalogues': other_catalogues}
    return render(request, 'admin/group.html', context)


@login_required
@admin_required
def add_catalogue_to_group(request):
    """Добавить каталог к группе"""
    form = GroupCatalogueForm(request.POST)
    if form.is_valid():
        try:
            Group.add_catalogue(form.cleaned_data['group_id'],
                                form.cleaned_data['catalogue_id'],
                                form.cleaned_data['permission'])
        except Exception as e:
            messages.warning(request, e)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@admin_required
def change_catalogues_in_group(request):
    """Изменить/удалить каталог из группы"""
    form = GroupCatalogueForm(request.POST)
    if form.is_valid():
        group_id = form.cleaned_data['group_id']
        catalogue_id = form.cleaned_data['catalogue_id']
        permission = form.cleaned_data['permission']
        if form.cleaned_data['action'] == 'save':
            Group.update_permission_in_catalogue(group_id, catalogue_id, permission)
        elif form.cleaned_data['action'] == 'delete':
            Group.delete_catalogue(group_id, catalogue_id)
        else:
            messages.warning(request, 'Unexpected action type')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@admin_required
def users_report(request):
    t = request.GET.get('report_type', '')
    if t == 'pdf':
        report = report_factory.create_report(ReportType.users_pdf)
        response = HttpResponse(report.get_report(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=users_report.pdf'
    elif t == 'csv':
        report = report_factory.create_report(ReportType.users_csv)
        response = HttpResponse(report.get_report(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users_report.csv"'
    else:
        response = redirect(request.META.get('HTTP_REFERER', '/'))
    return response


@login_required
@admin_required
def groups_report(request):
    t = request.GET.get('report_type', '')
    if t == 'pdf':
        report = report_factory.create_report(ReportType.groups_pdf)
        response = HttpResponse(report.get_report(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=groups_report.pdf'
    elif t == 'csv':
        report = report_factory.create_report(ReportType.groups_csv)
        response = HttpResponse(report.get_report(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="groups_report.csv"'
    else:
        response = redirect(request.META.get('HTTP_REFERER', '/'))
    return response
