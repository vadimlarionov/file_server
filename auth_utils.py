from functools import wraps
from string import ascii_letters, digits
import random

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


def create_session_key(size=24):
    chars = ascii_letters + digits
    return ''.join(random.choice(chars) for _ in range(size))
