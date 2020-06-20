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
            print('Intercepted Request Path:', path)
            if path == '/auth/callback':
                print('Detected OAuth Callback...')
                print('OAuth CallBack Code Parameter:', request.GET.get('code',"nothing"))

        # Retrieve Code From Callback and Store in Sessoin
        if path == '/auth/callback':
            code = request.GET.get('code')
            post_data = urlencode({
                'code': code, 
                'grant_type': 'authorization_code',
                'response_type': 'token',
                'client_id': settings.UAA_CLIENT_ID,
                'client_secret': settings.UAA_CLIENT_SECRET,
            })
            request.session['token_post_data'] = post_data

            # DEBUG output
            if settings.DEBUG:
                print('Encoded Code Post:', post_data)
                
        response = self.get_response(request)

        return response
