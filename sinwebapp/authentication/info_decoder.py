from core import settings
from django.contrib.auth.models import User

def decodeUserInfo(request):
    
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))

    user_id = request.session['_auth_user_id']
    this_user = User.objects.get(id=user_id)
    print(this_user.email)
