from functools import wraps


def throws(e):
    def deco(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except e:
                raise e
        return wrapped
    return deco
