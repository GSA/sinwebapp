from django.http import JsonResponse
from debug import DebugLogger
from django.contrib.auth.models import Group, User
from api.models import Sin, Status

# GET: /api/user
# 
# Description: retrieves user associated with request
def user_info(request):

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
        response = {
                'email': request.user.email,
               'groups': group_list
        } 
    else:
        response = { 'message': "No User Signed In" }

    return JsonResponse(response, safe=False)

# GET: /api/sin?id=123456 { body: empty }
# POST: /api/sin { body: new SIN }
#
# Description: retrieves information for a specific SIN number or posts a new SIN
def sin_info(request):
    
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['content']
        user_id = User.objects.get(email=request.user.email).id
    
    if request.method == "GET":
        logger = DebugLogger("sinwebapp.api.views.get_sin_info").get_logger()
        logger.info('Retrieving SIN Info...')

        sin=request.GET.get('id','')
        logger.info('SIN Number: %s', sin)    

        if not sin:
            retrieved_sin ={ 'message': 'Input Error' }
            logger.info('Parameter Not Provided')
        else:
            try:
                raw_sin = Sin.objects.get(sin_number=sin)
                retrieved_sin = {
                    'sin_number': raw_sin.sin_number,
                    'user': raw_sin.user,
                    'status': raw_sin.status
                }
                logger.info('SIN Found!')
            except Sin.DoesNotExist:
                retrieved_sin = { 'message': 'SIN Does Not Exist' }
                logger.info('SIN Not Found!')

        return JsonResponse(retrieved_sin, safe=False)

# GET: /api/sins
#
# Description: retrieves information on all SIN numbers
def sin_info_all(request):
    logger = DebugLogger("sinwebapp.api.views.get_all_sins_info").get_logger()
    logger.info('Retrieving All SIN Info...')

    try:
        retrieved_sins = list(Sin.objects.values())
    except Sin.DoesNotExist:
        retrieved_sins = { 'message': 'SINs Do Not Exist' }
        logger.info('SINs Not Found!')
    if len(retrieved_sins) == 0:
        retrieved_sins = { 'message': '0 SINs found' }
        logger.info('No SINs Found!')
    else:
        logger.info('SINs Found!')

    return JsonResponse(retrieved_sins, safe=False)

# GETl /api/status?id=1
# 
# Description: retrieves information for a specific Status
def status_info(request):
    logger = DebugLogger("sinwebapp.api.views.get_status_info").get_logger()
    logger.info('Retrieving Status Info...')

    status_id=request.GET.get('id','')
    logger.info('Status Id: %s', status_id)

    if not status_id:
        retrieved_status = { 'message': 'Input Error' }
        logger.info('Parameter Not Provided')

    try:
        raw_status = Status.objects.get(id=status_id)
        retrieved_status = {
            'status' : raw_status.status,
            'description': raw_status.description,
        }
        logger.info('Status Found!')
    except Status.DoesNotExist:
        retrieved_status = { 'message': 'Status Does Not Exist' }
        logger.info('Status Not Found!')

    return JsonResponse(retrieved_status, safe=False)