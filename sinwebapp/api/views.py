import json 

from django.http import JsonResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from api.models import Sin, Status
from api.models import STATUS_STATES, SIN_FIELDS
from authentication.db_init import GROUPS

from debug import DebugLogger

# GET: /api/user
# 
# Description: retrieves user associated with request
def user_info(request):
    logger = DebugLogger("sinwebapp.api.views.user_info").get_logger()
    logger.info('Retrieving User Info...')
    logger.info('Request Email: %s', request.user.email)
    logger.info('Request User Groups: %s', request.user.groups)

    if hasattr(request.user, 'email') and hasattr(request.user, 'groups'):

        group_list = list(request.user.groups.values_list('name',flat = True)) 
        response = {
                'id': request.user.id,
                'email': request.user.email,
               'groups': group_list
        } 
    else:
        response = { 'message': "No User Signed In" }

    return JsonResponse(response, safe=False)

# GET: /api/users?ids=1&ids=2&ids=3
#
# Description: Retrieves an array of users with the ids provided in the array parameter.
@login_required
def user_info_filtered(request):
    logger = DebugLogger("sinwebapp.api.views.user_info_filtered").get_logger()
    logger.info('Retrieving Users')

    if 'ids' in request.GET:
        ids = request.GET.getlist('ids')
        logger.info('Using Query Parameter IDs array: %s', ids)
        try:
            raw_users = User.objects.filter(id__in=ids)
            retrieved_users = []
            # TODO: CHECK IF LENGTH IS ZERO
            for user in raw_users.all():
                group_list = list(user.groups.values_list('name', flat=True))
                retrieved_users.append({
                    'id': user.id,
                    'email': user.email,
                    'groups': group_list
                })
            logger.info('Users Found!')
        except User.DoesNotExist:
            retrieved_users = { 'message' : 'Users Do No Exist'}
            logger.info('Users Not Found!')
    else:
        retrieved_users = { 'message': 'Input Error' }
        logger.info('No Query Parameters Provided')

    return JsonResponse(retrieved_users, safe=False)

# GET: /api/sinUser?user_id=123
#
# Description: Retrieved information about a given user based on
# the provided id.
@login_required
def sin_user_info(request):
    logger = DebugLogger("sinwebapp.api.views.sin_user_info").get_logger()
    logger.info('Retrieving User Info From SIN User ID')

    if 'user_id' in request.GET:
        user_id = request.GET.get('user_id')
        logger.info('Using User ID Query Parameter: %s', user_id)
        try:
            raw_user = User.objects.get(id=user_id)
            # TODO: Check if length is zero
            group_list = list(raw_user.groups.values_list('name', flat=True))
            logger.info('User Found!')
            retrieved_user = {
                'id': user_id,
                'email': raw_user.email,
                'groups': group_list
            }
        except User.DoesNotExist:
            retrieved_user = { 'message': 'User Does Not Exist' }
            logger.warning('User Not Found!')
    else:
        retrieved_user = { 'message': 'Input Error' }
        logger.info('No Query Parameters Provided')

    return JsonResponse(retrieved_user, safe=False)

@login_required
def sin_info_update(request):
    logger = DebugLogger("sinwebapp.api.views.sin_info_update").get_logger()
    logger.info('Updating Existing SIN')

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    body_keys = list(body.keys())
    parameter_check = True

    for key, parameter in SIN_FIELDS.items():
        if parameter not in body_keys:
            parameter_check = False

    if parameter_check:

        sin_id = body[SIN_FIELDS[1]]
        sin_number = body[SIN_FIELDS[2]]
        user_id = body[SIN_FIELDS[3]]
        status_id = body[SIN_FIELDS[4]]
        sin_description = body[SIN_FIELDS[5]]
        sin_title = body[SIN_FIELDS[7]]

        try:
            new_status = Status.objects.get(id=status_id)
            logger.info('Status Found')
            try:
                new_user = User.objects.get(id=user_id)
                logger.info('User Found')
                try:
                    new_sin = Sin(id=sin_id, sin_number=sin_number, status=new_status, user=new_user,
                                    sin_group_title=sin_title, sin_description1=sin_description)
                    logger.info('SIN Found')   
                    new_sin.save()
                    response={
                        SIN_FIELDS[1]: sin_id,
                        SIN_FIELDS[2]: sin_number,
                        SIN_FIELDS[3]: new_status.id,
                        SIN_FIELDS[4]: new_user.id,
                        SIN_FIELDS[5]: sin_description,
                        SIN_FIELDS[7]: sin_title
                    }
                except Sin.DoesNotExist:
                    response = { 'message': 'SIN Does Not Exist'}
                    logger.info('SIN Not Found')    
            except User.DoesNotExist:
                response = { 'message': 'User Does Not Exist'}
                logger.info('User Not Found')
        except Status.DoesNotExist:
            response = { 'message' : 'Status Does Not Exist'}
            logger.info('Status Not Found')
    
    else:

        response = { 'message' : 'Body Parameter Parsing Error'}
        logger.info('Error Parsing Parameters in Request Body')

    return JsonResponse(response, safe=False)

# GET: /api/sin?id=123456 { body: empty }
# POST: /api/sin { body: new SIN }
# 
# Description: retrieves information for a specific SIN number or posts a new SIN
# Post should be of form:
# { 
#   'sin_number': 123456
# }
@login_required
def sin_info(request):
    
    logger = DebugLogger("sinwebapp.api.views.sin_info").get_logger()

    # Posting new SIN to database or modifying inactive existing SIN
    if request.method == "POST":
        logger.info('Posting New SIN')

        if hasattr(request.user, 'email'):
            email = request.user.email
            logger.info('User Posting: %s', email)
        else:
            logger.warning('No User Associated With Incoming Request')
            return JsonResponse({ 'error': 'No User Signed In.' })
 
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # TODO 1: use SIN_FIELDS array to verify body contains all parameters
        # TODO 2: use SIN_FIELDS array to pull all fields from body automatically
        # instead of doing it manually
        sin_number = body['sin_number']
        sin_title = body['sin_group_title']
        sin_description = body['sin_description1']

        logger.info('SIN # Posting: %s', sin_number)

        # create submitted status
        new_status = Status.objects.get(id=1)
        logger.info('Status Posting: %s', new_status.name)

        # verify sin is not already active
        logger.info('Attempting To Post...')
        try: 
            sin = Sin.objects.get(sin_number=sin_number)
            logger.info('SIN # Exists!')
            if sin.status in [1,2,3]:
                # STATUS STATES:  
                # 1 = submitted, 2 = reviewed, 3 = change
                # 4 = approved, 5 = denied, 6 = expired
                logger.warning('Existing SIN Cannot Be Modified')
                return JsonResponse({ 'error': 'Existing SIN # Still In Process.' })
                
            else:
                sin.update(user=request.user, status=new_status)
                logger.info('Existing SIN # Updated.')
                return JsonResponse(sin, safe=False)
        
        # post new sin
        except Sin.DoesNotExist:
            sin = Sin.objects.create(sin_number=sin_number, user=request.user, status=new_status,
                                        sin_group_title=sin_title, sin_description1=sin_description)
            sin.save()
            logger.info('New SIN # Posted')
            # TODO: determine how to serialize django model instead of doing this manually
            raw_sin = {
                'id': sin.id,
                'sin_number': sin.sin_number,
                'user_id': request.user.id,
                'status_id': new_status.id,
                'sin_group_title': sin.sin_group_title,
                'sin_description1': sin.sin_description1
            }
            return JsonResponse(raw_sin, safe=False)
            
    # retrieving information on a specific SIN
    if request.method == "GET":
        logger.info('Retrieving SIN Info')

        if 'id' in request.GET:
            sin=request.GET.get('id')
            logger.info('Using ID Query Parameter: %s', sin)

            try:
                # TODO: figure out how to serialize model instance directly like 
                # is done below with lists of SINS
                raw_sin = Sin.objects.get(sin_number=sin)
                retrieved_sin = {
                    'id': raw_sin.id,
                    'sin_number': raw_sin.sin_number,
                    'user_id': raw_sin.user.id,
                    'status_id': raw_sin.status.id,
                    'sin_group_title': raw_sin.sin_group_title,
                    'sin_description1': raw_sin.sin_description1,
                    'sin_description2': raw_sin.sin_description2
                }
                logger.info('SIN Found!')
            except Sin.DoesNotExist:
                retrieved_sin = { 'message': 'SIN Does Not Exist' }
                logger.warning('SIN Not Found!')

        elif 'user_email' in request.GET:
            user_email = request.GET.get('user_email')
            logger.info('Using User Email Query Parameter: %s', user_email)
            try:
                search_user = User.objects.get(email=user_email)
                logger.info('User Found!')
                retrieved_sin = list(Sin.objects.filter(user=search_user).values())
            except User.DoesNotExist:
                retrieved_sin = { 'message': 'User Does Not Exist'}
                logger.warning('User Not Found!')

        elif 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            logger.info('Using User Id Query Parameter: %s', user_id)
            try:
                search_user = User.objects.get(id=user_id)
                logger.info('User Found!')
                retrieved_sin = list(Sin.objects.filter(user=search_user).values())
            except User.DoesNotExist:
                retrieved_sin = {'message': 'User Does Not Exist'}
                logger.warning('User Not Found!')

        elif 'status' in request.GET:
            user_status = request.GET.get('status') 
            logger.info('Using Status Query Parameter: %s', user_status)
            try:  
                search_status = Status.objects.get(id=user_status)
                logger.info('Status Found!')
                retrieved_sin = list(Sin.objects.filter(status=search_status).values()) 
            except User.DoesNotExist:
                retrieved_sin = { 'message': 'Status Does Not Exist' }
                logger.warning('Status Not Found!')
        else:
            retrieved_sin ={ 'message': 'Input Error' }
            logger.info('No Query Parameters Provided')

        return JsonResponse(retrieved_sin, safe=False)

# GET: /api/sins
#
# Description: retrieves information on all SIN numbers
@login_required
def sin_info_all(request):
    logger = DebugLogger("sinwebapp.api.views.sins_info_all").get_logger()
    logger.info('Retrieving All SIN Info...')

    try:
        retrieved_sins = list(Sin.objects.values())
        if len(retrieved_sins) == 0:
            retrieved_sins = { 'message': '0 SINs found' }
            logger.info('0 SINs Found!')
        else:
            logger.info('SINs Found!')
    except Sin.DoesNotExist:
        retrieved_sins = { 'message': 'SINs Do Not Exist' }
        logger.info('SINs Not Found!')

    return JsonResponse(retrieved_sins, safe=False)

# GET: /api/status?id=1
# 
# Description: retrieves information for a specific Status
@login_required
def status_info(request):
    logger = DebugLogger("sinwebapp.api.views.status_info").get_logger()
    logger.info('Retrieving Status Info')

    if 'id' in request.GET:
        status_id=request.GET.get('status_id')
        logger.info('Using Status Id Query Parameter: %s', status_id)
        try:
            raw_status = Status.objects.get(id=status_id)
            retrieved_status = {
                'id': raw_status.id,
                'name' : raw_status.name,
                'description': raw_status.description,
            }
            logger.info('Status Found!')
        except Status.DoesNotExist:
            retrieved_status = { 'message': 'Status Does Not Exist' }
            logger.info('Status Not Found!')
    else:
        retrieved_status = { 'message': 'Input Error' }
        logger.info('Parameter Not Provided')

    return JsonResponse(retrieved_status, safe=False)

# GET: /api/statuses
#
# Description: Retrieves a list of all Statuses accessible by the user
# signed into the request's session
@login_required
def user_status_info(request):
    logger = DebugLogger('sinwebapp.api.views.user_status_info').get_logger()
    logger.info('Retrieving All Statuses')

    try:
        group_list = request.user.groups.values_list('name', flat=True)
        if GROUPS['submitter'] in group_list:
            retrieved_statuses = list(Status.objects.filter(id__in=[STATUS_STATES['submitted']]).values())
            logger.info('Status Found!')
        elif GROUPS['reviewer'] in group_list:
            retrieved_statuses = list(Status.objects.filter(id__in=[STATUS_STATES['submitted'],
                                                                    STATUS_STATES['reviewed'],
                                                                    STATUS_STATES['change']]).values())
            logger.info('Statuses Found!')
        elif GROUPS['approver'] in group_list or GROUPS['admin'] in group_list:
            retrieved_statuses = list(Status.objects.values())
            logger.info('Statuses Found!')
        else:
            retreived_statuses = { 'message' : 'User Does Not Have Any Permissions'}
            logger.info('User Has No Permissions!')

    except Status.DoesNotExist:
        retrieved_statuses = {'message': 'Statuses Do Not Exist'}
        logger.info('Statuses Not Found!')
        
    return JsonResponse(retrieved_statuses, safe=False)

@login_required
def status_info_all(request):
    logger = DebugLogger('sinwebapp.api.views.status_info_all').get_logger()
    logger.info('Retrieving All Statuses')

    try:
        group_list = request.user.groups.values_list('name', flat=True)
        retrieved_statuses = list(Status.objects.values())
        if len(retrieved_statuses)==0:
            retrieved_statues = { 'message' : '0 Statuses Found' }
            logger.info('0 Statuses Found!')
        else:
            logger.info('Statuses Found!')
    except Status.DoesNotExist:
        retrieved_statuses = {'message': 'Statuses Do Not Exist'}
        logger.info('Statuses Not Found!')
        
    return JsonResponse(retrieved_statuses, safe=False)