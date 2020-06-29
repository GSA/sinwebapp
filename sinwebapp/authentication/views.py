from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_page(request):
    return render(request, 'login_splash.html')

@login_required
def login_success_page(request):
    context= { 'user_email': request.user.email }
    return render(request, 'login_success.html', context)
    
def logout_page(request):
    logout(request)
    return render(request, 'logout_splash.html')
