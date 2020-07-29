from django.http import JsonResponse
from debug import DebugLogger
from django.contrib.auth.models import Group, User
from api.models import Sin, Status

# /api/user

# retrieves user associated with request
def get_user_info(request):

    logger = DebugLogger("sinwebapp.api.views.get_user_info").get_logger()
    logger.info('Retrieving User Info...')
    logger.info('Request Email: %s', request.user.email)
    logger.info('Request User Groups: %s', request.user.groups)

    if hasattr(request.user, 'email'):
        
        if not hasattr(request.user, 'groups'):
            logger.info('User Has No Group, Assigning Default Group...')
            approver_group = Group.objects.get(name='submitter_group')
            user_object = User.objects.get(email=request.user.email)
            approver_group.user_set.add(user_object)

        user_groups = request.user.groups.values_list('name',flat = True)
        group_list = list(user_groups) 
        response = JsonResponse({
                'email': request.user.email,
               'groups': group_list
        }) 
    else:
        response = JsonResponse({
            'message': "No User Signed In"
        })

    return response

# /api/sin?number=123456
# retrieves information for a specific SIN number
def get_sin_info(request):
    logger = DebugLogger("sinwebapp.api.views.get_sin_info").get_logger()
    logger.info('Retrieving SIN Info...')

    sin=request.GET.get('number','')
    logger.info('SIN Number: %s', sin)    

    if not sin:
        retrieved_sin ={
            'message': 'Input Error'
        }
        logger.info('Parameter Not Provided')
    else:
        try:
            retrieved_sin = Sin.objects.get(sin_number=sin)
            logger.info('SIN Found!')
        except Sin.DoesNotExist:
            retrieved_sin = {
                'message': 'SIN Does Not Exist'
            }
            logger.info('SIN Not Found!')

    response = JsonResponse(retrieved_sin, safe=False)

# /api/sins
# retrieves information on all SIN numbers
def get_all_sins_info(request):
    logger = DebugLogger("sinwebapp.api.views.get_all_sins_info").get_logger()
    logger.info('Retrieving All SIN Info...')

    try:
        retrieved_sins = list(Sin.objects.values())
        logger.info('SINs Found!')
    except Sin.DoesNotExist:
        retrieved_sins = {
            'message': 'SINs Do Not Exist'
        }
        logger.info('SINs Not Found!')
    if len(retrieved_sins) == 0:
            retrieved_sins = {
                'message': '0 SINs found'
            }
            logger.info('No SINs Found!')
    return JsonResponse(retrieved_sins, safe=False)

# /api/status?id=1
# retrieves information for a specific Status
def get_status_info(request):
    logger = DebugLogger("sinwebapp.api.views.get_status_info").get_logger()
    logger.info('Retrieving Status Info...')

    status_id=request.GET.get('id','')
    logger.info('Status Id: %s', status_id)

    if not status_id:
        retrieved_status = {
            'message': 'Input Error'
        }

    try:
        retrieved_status = Status.objects.get(id=status_id)
    except Status.DoesNotExist:
        retrieved_status = {
            'message': 'Status Does Not Exist'
        }
    return JsonResponse(retrieved_status, safe=False)