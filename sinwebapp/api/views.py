from django.http import JsonResponse

def user_info(request):
    return JsonResponse({
        'email': request.user.email
    })