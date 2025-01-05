import functools
from flask import session, jsonify
from http import HTTPStatus

def require_login(org_func = None):
    def decorator_require_login(func):
        @functools.wraps(func)
        def wrapper_require_login(*args, **kwargs):
            if session.get('address'):
                return func(*args, **kwargs)
            else:
                return jsonify({'message': 'User not logged in'}), HTTPStatus.UNAUTHORIZED
        return wrapper_require_login
    if org_func:
        return decorator_require_login(org_func)
    else:
        return decorator_require_login