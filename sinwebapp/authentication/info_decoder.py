import requests
import jwt
from core import settings

def decodeUserInfo(request):
    post_code = request.session['token_code']
    post_data = {
        'code': post_code, 
        'grant_type': 'authorization_code',
        'response_type': 'token',
        'client_id': settings.UAA_CLIENT_ID,
        'client_secret': settings.UAA_CLIENT_SECRET,
    }

    if settings.DEBUG:
        print('decodeUserInfo:', 'settings.UAA_TOKEN_URL:', settings.UAA_TOKEN_URL)
        print('decodeUserInfo:', 'Token Post Data:', post_data)

    post = requests.post(settings.UAA_TOKEN_URL, post_data)
    post_response = post.text

    if settings.DEBUG:
        print('decodeUserInfo:', 'Token Post Response: ', post_response)
        
    # exchange code for token
    # TODO: decode token
    # TODO: save user info in session 