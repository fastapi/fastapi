from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # login functionality could come here
        return func(*args, **kwargs)

    return wrapper
