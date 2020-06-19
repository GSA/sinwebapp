from django.shortcuts import render

def login_page(request):
    return render(request, 'login_splash.html')

def login_success(request):
    return render(request, 'login_success.html')
    
def logout_page(request):
    return render(request, 'logout_splash.html')

