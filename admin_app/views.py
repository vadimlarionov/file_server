from django.shortcuts import render, redirect

from admin_app.forms import LoginForm
from auth_utils import login_required
from admin_app.db_service import DbService
from admin_app.data_access_layer.active_records import *


@login_required
def index(request):
    print('index view')
    user = UserActiveRecord.find(1)
    user.delete()
    context = dict()
    return render(request, 'index.html', context)


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

    db_service = DbService()
    db_service.execute()

    response = redirect('/')
    response.set_cookie('foo', 'bar')
    return response
