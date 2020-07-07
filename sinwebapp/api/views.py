from django.http import JsonResponse
from debug import DebugLogger

def user_info(request):

    logger = DebugLogger("sinwebapp.api.views.user_info").get_logger()
    logger.info('Retrieving User Info...')
    logger.info('Request User: %s', request.user.username)
    logger.info('Request Email: %s', request.user.email)
    logger.info('Request First Name: %s', request.user.first_name)
    logger.info('Request Last Name: %s', request.user.last_name)
    logger.info('Request User Groups: %s', request.user.groups)

    if hasattr(request.user, 'email'):
        response = JsonResponse({
            'email': request.user.email,
        }) 
    else:
        response = JsonResponse({
            'error': "NO USER SIGNED IN"
        })

    return response