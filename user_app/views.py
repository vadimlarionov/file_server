from collections import namedtuple

from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.

from auth_utils import login_required
from user_app.business_logic_layer.transact_script import TransactionScript as Ts
from user_app.forms import (AddCatalogueForm, UploadFileForm,
                            FileDeleteForm, CatalogueDeleteForm)


@login_required
def list_catalogues(request, user_id):
    """Вывод каталогов пользователя."""
    CalatogueWithDeleteForm = namedtuple('CalatogueWithDeleteForm', ['catalogue', 'form'])
    catalogues_with_forms = {CalatogueWithDeleteForm(catalogue,
                                                     CatalogueDeleteForm({'catalogue_id': catalogue.id})):
                             catalogue for catalogue in Ts.get_user_catalogues(user_id)}
    return render(request, 'user/catalogues_list.html', context={'catalogues': catalogues_with_forms})


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
    FileWithDeleteForm = namedtuple('FileWithDeleteForm', ['file', 'form'])
    files_with_forms = {FileWithDeleteForm(file, FileDeleteForm({'file_id': file.id})):
                        file for file in Ts.get_catalogue_files(cat_id)}
    cat = Ts.get_catalogue(cat_id)
    return render(request, 'user/catalogue.html', context={'files': files_with_forms,
                                                           'catalogue': cat})


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
