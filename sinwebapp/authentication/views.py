from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.user_info import retrieveUserEmail

def login_page(request):
    return render(request, 'login_splash.html')

@login_required
def login_success(request):
    user_email = retrieveUserEmail(request)
    return render(request, 'login_success.html', {'user_email': user_email})
    
def logout_page(request):
    return render(request, 'logout_splash.html')
