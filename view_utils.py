from django.http import HttpResponse


def not_implemented(*_, **__):
    """
    Not implemented HTTP response for Django view functions
    :param _: Captures all normal arguments
    :param __: Captures all keyword arguments
    :return: An HTTP response
    """
    return HttpResponse('<h1>Not implemented yet!<h1>')
