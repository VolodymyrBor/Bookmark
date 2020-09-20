from functools import wraps

from django.http import HttpResponseBadRequest, HttpRequest


def ajax_required(func):
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return func(request, *args, **kwargs)
    return wrapper
