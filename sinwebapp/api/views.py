from django.http import JsonResponse

def user_info(request):
    if hasattr(request.user, 'email'):
        response = JsonResponse({
            'email': request.user.email
        })
    else:
        response = JsonResponse({
            'error': "No user signed in"
        })
    return response