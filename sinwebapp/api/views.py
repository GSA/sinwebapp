from django.http import JsonResponse
from debug import DebugLogger

def user_info(request):

    logger = DebugLogger("sinwebapp.api.views.user_info").get_logger()
    logger.info('Retrieving User Info...')
    logger.info('Request User: %s', request.user.username)
    logger.info('Request Email: %s', request.user.email)
    logger.info('Request First Name: %s', request.user.first_name)
    logger.info('Request Last Name: %s', request.user.last_name)

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