from functools import wraps

from django.shortcuts import redirect


def login_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return function(request, *args, **kwargs)
    return wrapper


def admin_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('/')
        return function(request, *args, **kwargs)
    return wrapper
