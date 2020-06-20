from urllib.request import urlopen
import jwt
from sinapp import settings

def decodeUserInfo(request):
    params = request.session['encoded_post_data']
    post = urlopen(settings.UAA_TOKEN_URL, params)
    post_response = post.read()
    print(post_response)
    # exchange code for token
    # decode token
    # save user info in session 