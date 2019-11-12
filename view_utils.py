from functools import wraps

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect


def not_implemented(*_, **__):
    """
    Not implemented HTTP response for Django view functions
    :param _: Captures all normal arguments
    :param __: Captures all keyword arguments
    :return: An HTTP response
    """
    return HttpResponse('<h1>Not implemented yet!<h1>')


def get_previous_url(req):
    """
    Returns the referrer (previous page before being sent here) of the request
    :param req: The request
    :return: The URL of the referrer as a string
    """
    return req.META.get('HTTP_REFERER', '/')


def get_previous_url_as_redirect(req):
    """
    Returns the referrer (previous page before being sent here) of the request
    :param req: The request
    :return: The URL of the referrer wrapped in a HttpResponseRedirect object
    """
    return HttpResponseRedirect(req.META.get('HTTP_REFERER', '/'))


def superuser_required(url_pattern_name):
    """
    Decorator that checks if the user is a superuser and displaying an error if not
    :param url_pattern_name: The URL pattern name of the URL to redirect to if the user is not a superuser
    :return:
    """

    def inner_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            req = args[0]
            if req.user.is_superuser:
                return func(*args, **kwargs)
            else:
                messages.error(req, 'You must be superuser to do that!')
                return redirect(url_pattern_name)

        return wrapper

    return inner_func
