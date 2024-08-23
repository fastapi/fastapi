from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("login")
        return func(*args, **kwargs)

    return wrapper
