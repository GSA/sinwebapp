from django.http import JsonResponse

def user_info(request):
    if hasattr(request.user, 'email'):
        response = JsonResponse({
            'email': request.user.email,
            'name': 'Ted Danson'
        }) 
    else:
        response = JsonResponse({
            'error': "No user signed in"
        })
    return response