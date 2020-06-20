from django.contrib.auth.models import User

def retrieveUserEmail(request):
    user_id = request.session['_auth_user_id']
    this_user = User.objects.get(id=user_id)
    print('authentication.retrieveUserEmail:', this_user.email)
    return this_user.email
