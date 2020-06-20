from urllib.parse import urlencode
from django.http.request import HttpRequest
from . import settings

class UserInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        path=request.path

        # DEBUG output
        if settings.DEBUG:
            print('UserInfoMiddelware:','Intercepted Request Path:', path)
            if path == '/auth/callback':
                print('UserInfoMiddelware:','Detected OAuth Callback...')
                print('UserInfoMiddelware:','OAuth CallBack Code Parameter:', request.GET.get('code'))

        # Retrieve Code From Callback and Store in Sessoin
        if path == '/auth/callback':
            code = request.GET.get('code')
            request.session['token_code'] = code
                
        response = self.get_response(request)

        return response
