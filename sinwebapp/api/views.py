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
            'message': "No User Signed In"
        })

    return response

# /api/sin?number=123456
def get_sin_info(request):
    sin=request.GET.get('number','')

    if not sin:
        retrieved_sin ={
            'message': 'Input Error'
        }
    else:
        try:
            retrieved_sin = Sin.objects.get(sin_number=sin)
        except Sin.DoesNotExist:
            retrieved_sin = {
                'message': 'SIN Does Not Exist'
            }

    response = JsonResponse({
        'sin_number': retrieved_sin.sin_number,
        'user': retrieved_sin.user,
        'status': retreived_sin.user
    })

# /api/sins
def get_all_sins_info(request):
    try:
        retrieved_sins = list(Sin.objects.values())
    except Sin.DoesNotExist:
        retrieved_sins = {
            'message': 'SINs Do Not Exist'
        }
    if len(retrieved_sins) == 0:
            retrieved_sins = {
                'message': '0 SINs found'
            }
    return JsonResponse(retrieved_sins, safe=False)

# /api/status?id=1
def get_status_info(request):
    status_id=request.GET.get('id','')

    if not status:
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