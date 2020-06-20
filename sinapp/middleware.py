from django.http.request import HttpRequest
from . import settings

class UserInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        # code goes here
        path=request.path
        code=request.GET.get('code',"nothing")
        if settings.DEBUG:
            print('request path', path)
            print('oauth code', code)

        response = self.get_response(request)

        return response
