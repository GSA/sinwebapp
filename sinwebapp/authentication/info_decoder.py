import requests
import jwt
from core import settings

def decodeUserInfo(request):
    encoded_post_data = request.session['token_post_data']

    if settings.DEBUG:
        print('decodeUserInfo:', 'settings.UAA_TOKEN_URL:', settings.UAA_TOKEN_URL)

    post = requests.post(settings.UAA_TOKEN_URL, encoded_post_data)
    post_response = post.text
    if settings.DEBUG:
        print('decodeUserInfo:', 'Token Post Response: ', post_response)
    # exchange code for token
    # TODO: decode token
    # TODO: save user info in session 