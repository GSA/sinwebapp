from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import info_decoder

def login_page(request):
    return render(request, 'login_splash.html')

@login_required
def login_success(request):
    info_decoder(request)
    return render(request, 'login_success.html')
    
def logout_page(request):
    return render(request, 'logout_splash.html')

