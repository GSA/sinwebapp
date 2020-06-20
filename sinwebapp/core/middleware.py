from urllib.parse import urlencode
from django.http.request import HttpRequest
from . import settings

class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        path=request.path

        if settings.DEBUG:
            print('DebugMiddelware:','Intercepted Request Path:', path)
            if path == '/auth/callback':
                print('DebugMiddleware:','Detected OAuth Callback...')
                print('DebugMiddleware:','OAuth CallBack Code Parameter:', request.GET.get('code'))
                print('DebugMiddleware:', 'OAuth CallBack State Parameter', request.GET.get('state'))
                
        response = self.get_response(request)

        return response
