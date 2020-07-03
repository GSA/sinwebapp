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
    #response["Access-Control-Allow-Origin"] = "*"
    #response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response