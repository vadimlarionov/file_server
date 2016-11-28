from functools import wraps
from string import ascii_letters, digits
import random


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print('login decorator')
        return function(*args, **kwargs)

    return wrapper


def create_session_key(size=24):
    chars = ascii_letters + digits
    return ''.join(random.choice(chars) for _ in range(size))
