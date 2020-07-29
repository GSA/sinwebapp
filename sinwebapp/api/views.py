from django.http import JsonResponse
from debug import DebugLogger
from django.contrib.auth.models import Group, User
from api.models import Sin, Status

def get_user_info(request):

    logger = DebugLogger("sinwebapp.api.views.user_info").get_logger()
    logger.info('Retrieving User Info...')
    logger.info('Request User: %s', request.user.username)
    logger.info('Request Email: %s', request.user.email)
    logger.info('Request First Name: %s', request.user.first_name)
    logger.info('Request Last Name: %s', request.user.last_name)
    logger.info('Request User Groups: %s', request.user.groups)

    if hasattr(request.user, 'email'):
        
        if not hasattr(request.user, 'groups'):
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
            'error': "NO USER SIGNED IN"
        })

    return response

# /api/sin?number=123456
def get_sin_info(request):
    sin=request.GET.get('number','')

    try:
        retrieved_sin = Sin.objects.get(sin_number=sin)
    except Sin.DoesNotExist:
        retrieved_sin = {
            'sin_number': 'No SIN Found',
            'user': 'No User Found',
            'status': 'No Status Found'
        }

    response = JsonResponse({
        'sin_number': retrieved_sin.sin_number,
        'user': retrieved_sin.user,
        'status': retreived_sin.user
    })

# /api/sins
def get_all_sins_info(request):
    try:
        retrieved_sin = list(Sin.objects.values())
    except Sin.DoesNotExist:
        retrieved_sin = {
            'sin_number': 'No SIN Found',
            'user': 'No User Found',
            'status': 'No Status Found'
        }
    return JsonResponse(retrieved_sin)

# /api/status?id=1
def get_status_info(request):
    status_id=request.GET.get('id','')

    try:
        retrieved_status = Status.objects.get(id=status_id)
    except Status.DoesNotExist:
        retrieved_status = {
            'status': 'No Status Found',
            'description': 'No Description Found'
        }
    return JsonResponse(retrieved_status)