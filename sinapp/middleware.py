from urllib.parse import urlencode
from urllib.request import urlopen
import jwt
from django.http.request import HttpRequest
from . import settings

class UserInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.token_exchange_url = 'https://uaa.fr.cloud.gov/oauth/token'

    def __call__(self, request: HttpRequest):
        path=request.path

        # DEBUG output
        if settings.DEBUG:
            print('Intercepted Incoming Request Path:', path)
            if path == '/auth/callback':
                print('Detected OAuth Callback...')
                print('OAuth CallBack Code Parameter:', request.GET.get('code',"nothing"))

        # Retrieve User Info From Token
        if path == '/auth/callback':
            code = request.GET.get('code')
            params = urlencode({
                'code': code, 
                'grant_type': 'authorization_code',
                'response_type': 'token',
                'client_id': settings.UAA_CLIENT_ID,
                'client_secret': settings.UAA_CLIENT_SECRET,

            })
            post = urlopen(self.token_exchange_url, params)
            post_response = post.read()
            print(post_response)

            # exchange code for token
            # decode token
            # save user info in session 

        response = self.get_response(request)

        return response
