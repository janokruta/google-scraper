from django.http import HttpResponseServerError
from httplib2 import ServerNotFoundError


def check_server_connection(func):
    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except ServerNotFoundError:
            return HttpResponseServerError()

    return inner
