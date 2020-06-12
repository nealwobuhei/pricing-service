import functools  # we can use functool to tell decorated_function to take in the name and documentation of original fuc
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app


def requires_login(f: Callable) -> Callable:  # f is a callable function
    @functools.wraps(f)  # the original function just extended by this decorated_function
    def decorated_function(*args, **kwargs):  # the index will be replaced by this decorated_function
        if not session.get('email'):  # if there is no email inside the session variable
            flash('You need to be signed in for this page.', 'danger')  # flash place this message into a queue of messages and template can get this queues and display them to the user
            # category is 'danger', message is content
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)

    return decorated_function  # return function itself, not the decorated function execution


def requires_admin(f: Callable) -> Callable:
    """
    to check whether session email is set, and it matches the current 'app.config.get('ADMIN')'
    current.app: if there is a current app loaded, and you are currently serving the user a request
    then current app will have the value of the app, then you're currently using to respond to that user
    make sure the user is ADMIN before allowing them to access any particular endpoint
    :param f:
    :return:
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN', ''):
            flash('You need to be an administrator to access this page.', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)

    return decorated_function