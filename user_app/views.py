import os
from collections import namedtuple

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect


from auth_utils import login_required
from user_app.business_logic_layer.transact_script import (PERMISSION_WR,
                                                           PERMISSION_W,
                                                           PERMISSION_R,
                                                           TransactionScript as Ts)
from user_app.forms import (AddCatalogueForm, UploadFileForm,
                            FileDeleteForm, CatalogueDeleteForm, EditFileForm)


@login_required
def list_catalogues(request, user_id):
    """Вывод каталогов пользователя."""
    CalatogueWithDeleteForm = namedtuple('CalatogueWithDeleteForm', ['catalogue', 'form'])
    catalogues_with_forms = [CalatogueWithDeleteForm(catalogue, CatalogueDeleteForm({'catalogue_id': catalogue.id}))
                             for catalogue in Ts.get_user_catalogues(user_id)]
    shared_catalogues = Ts.get_shared_catalogues(user_id)
    return render(request, 'user/catalogues_list.html', context={'catalogues': catalogues_with_forms,
                                                                 'shared_catalogues': shared_catalogues})


@login_required
def add_catalogue(request):
    """Добавление каталога."""
    form = AddCatalogueForm(request.POST or None)
    try:
        if request.method == 'POST' and form.is_valid():
            catalogue = Ts.create_catalogue(form.cleaned_data['title'], request.user.id)
            if catalogue is not None:
                messages.success(request, 'Каталог "{}" создан'.format(catalogue.title))
            return redirect('/user/{}/catalogues'.format(request.user.id))
    except Exception as e:
        messages.warning(request, e)
    return render(request, 'user/catalogue_add.html', {'form': form})


@login_required
def catalogue_detail(request, cat_id):
    """Отобразить содержимое каталога."""
    permission = Ts.get_permission_on_catalogue(cat_id, request.user.id)
    FileWithDeleteForm = namedtuple('FileWithDeleteForm', ['file', 'form'])
    write_allowed = True if permission in (PERMISSION_W, PERMISSION_WR) else False
    read_allowed = True if permission in (PERMISSION_R, PERMISSION_WR) else False
    files = [FileWithDeleteForm(file, FileDeleteForm({'file_id': file.id}))
             for file in Ts.get_catalogue_files(cat_id)]
    cat = Ts.get_catalogue(cat_id)
    return render(request, 'user/catalogue.html', context={'files': files,
                                                           'catalogue': cat,
                                                           'write_allowed': write_allowed,
                                                           'read_allowed': read_allowed})


@login_required
def file_download(request, file_id):
    """Скачать файл."""
    file = Ts.get_file(file_id)
    data = Ts.download_file(file_id)

    response = HttpResponse(data)

    response['Content-Disposition'] = 'attachment; filename={file_name}'.format(
        file_name=os.path.basename(file.path)
    )

    return response


@login_required
def catalogue_download(request, cat_id):
    """Скачать каталог."""
    cat = Ts.get_catalogue(cat_id)
    data = Ts.download_catalogue(cat_id)

    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment; filename={}.zip'.format(cat.title)

    return response


@login_required
def file_detail(request, file_id):
    """Отобразить содержимое каталога."""
    file = Ts.get_file(file_id)
    return render(request, 'user/file.html', context={'file': file})


@login_required
def file_delete(request):
    """Выпилить файл."""
    form = FileDeleteForm(request.POST)
    if form.is_valid():
        Ts.delete_file(form.cleaned_data['file_id'])
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def catalogue_delete(request):
    """Выпилить файл."""
    form = CatalogueDeleteForm(request.POST)
    if form.is_valid():
        Ts.delete_catalogue(form.cleaned_data['catalogue_id'])
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def upload_file(request, cat_id):
    """Загрузить файл."""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            Ts.save_file(form.cleaned_data, request.user.id, cat_id)
            return redirect('/catalogue/{}'.format(cat_id))
    else:
        form = UploadFileForm()
    return render(request, 'user/file_upload.html', {'form': form, 'cat_id': cat_id})


@login_required
def edit_file(request, cat_id, file_id):
    """Редактировать файл."""
    if request.method == 'POST':
        form = EditFileForm(request.POST, request.FILES)
        if form.is_valid():
            Ts.edit_file(file_id, form.cleaned_data)
            return redirect('/catalogue/{}'.format(cat_id))
    else:
        file = Ts.get_file(file_id)
        form = EditFileForm(initial={
             'title': file.title,
             'description': file.description,
             'attributes': file.attributes,
             'other_attributes': file.other_attributes
        })
    return render(request, 'user/file_edit.html', {'form': form, 'cat_id': cat_id, 'file_id': file_id})
