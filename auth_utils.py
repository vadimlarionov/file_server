from functools import wraps


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print('login decorator')
        return function(*args, **kwargs)

    return wrapper
