from urllib.request import urlopen
import jwt
from core import settings

def decodeUserInfo(request):
    encoded_post_data = request.session['token_post_data'].encode('utf-8')
    post = urlopen(settings.UAA_TOKEN_URL, encoded_post_data)
    post_response = post.read()
    print(post_response)
    # exchange code for token
    # TODO: decode token
    # TODO: save user info in session 