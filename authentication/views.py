from django.shortcuts import render

def login_page(request):
    return render(request, 'login_splash.html')

def logout_page(request):
    return render(request, 'logout_splash.html')
