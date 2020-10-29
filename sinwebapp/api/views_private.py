import json 

from django.http import JsonResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from api.models import Sin, Status
from api.models import STATUS_STATES, SIN_FIELDS
from authentication.db_init import GROUPS
from api.email_manager import notify_reviewer, notify_approver, confirm_submitter, approve_submitter

from debug import DebugLogger

def verify_method(request, allowed_methods):
    if request.method not in allowed_methods: 
        return False
    else:
        return True

# GET: /api/user
# 
# Description: retrieves user associated with incoming request
def user_info(request):
    logger = DebugLogger("sinwebapp.api.views.user_info").get_logger()

    logger.info('Verifying Request Method')

    if verify_method(request, ["GET"]):

        logger.info('Request Method Verified')
        logger.info('Retrieving User Info')
        logger.info('Request Email: %s', request.user.email)
        logger.info('Request User Groups: %s', request.user.groups)

        if hasattr(request.user, 'email') and hasattr(request.user, 'groups'):

            group_list = list(request.user.groups.values_list('name',flat = True)) 
            response = {
                    'id': request.user.id,
                    'email': request.user.email,
                'groups': group_list
            } 
            return JsonResponse(response, safe=False)
        else:
            response = { 'message': "No User Signed In" }
            return JsonResponse(response, status=403, safe=False)
    else:

        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)



# GET: /api/users?ids=1&ids=2&ids=3
#
# Description: Retrieves an array of users with the ids provided in the array parameter.
@login_required
def user_info_filtered(request):
    logger = DebugLogger("sinwebapp.api.views.user_info_filtered").get_logger()

    logger.info('Verfiying Request Method')
    if verify_method(request, ["GET"]):

        logger.info('Request Method Verified')
        logger.info('Retrieving Users')

        if 'ids' in request.GET:
            ids = request.GET.getlist('ids')
            logger.info('Using Query Parameter IDs array: %s', ids)
            try:
                raw_users = User.objects.filter(id__in=ids)
                retrieved_users = []
                if len(list(raw_users)) == 0:
                    retrieved_users.append({ 'message' : '0 Users Found'})
                else:
                    for user in raw_users.all():
                        group_list = list(user.groups.values_list('name', flat=True))
                        retrieved_users.append({
                            'id': user.id,
                            'email': user.email,
                            'groups': group_list
                        })
                    logger.info('Users Found!')
                return JsonResponse(retrieved_users, safe=False)

            except User.DoesNotExist:
                retrieved_users = { 'message' : 'Users Do No Exist'}
                logger.info('Users Not Found!')
                return JsonResponse(retrieved_users, safe=False)

        else:
            retrieved_users = { 'message': 'Input Error' }
            logger.info('No Query Parameters Provided')
            return JsonResponse(retrieved_users, status=400, safe=False)
    
    else:

        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)

# GET: /api/sinUser?user_id=123
#
# Description: Retrieves information about a given user based on the provided id.
# TODO: This method/endpoint is potentially redundant.
@login_required
def sin_user_info(request):
    logger = DebugLogger("sinwebapp.api.views.sin_user_info").get_logger()

    logger.info('Verifying Request Method')

    if verify_method(request, ["GET"]):

        logger.info('Request Method Verified')
        logger.info('Retrieving User Info From SIN User ID')

        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            logger.info('Using User ID Query Parameter: %s', user_id)
            try:
                raw_user = User.objects.get(id=user_id)
                group_list = list(raw_user.groups.values_list('name', flat=True))
                logger.info('User Found!')
                retrieved_user = {
                    'id': user_id,
                    'email': raw_user.email,
                    'groups': group_list
                }
                return JsonResponse(retrieved_user, safe=False)

            except User.DoesNotExist:
                retrieved_user = { 'message': 'User Does Not Exist' }
                logger.warning('User Not Found!')
                return JsonResponse(retrieved_user, status=404, safe=False)

        else:
            retrieved_user = { 'message': 'Input Error' }
            logger.info('No Query Parameters Provided')
            return JsonResponse(retrieved_user, status=400, safe=False)

    else:

        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)

# POST: /api/sinUpdate
# { body:{
#   'sin_id': id
#   'sin_number': 'number'
#   'user_id': new id,
#   'status_id': new id
#   'sin_description': 'new description' 
#   'sin_title': 'new title'
#   }
# }
# 
# This POST method will override any SIN with new fields supplied in the body parameters.
# This endpoint is used to process submitted SINs as they are reviewed and approved through
# the SIN workflow.
@login_required
def sin_info_update(request):
    logger = DebugLogger("sinwebapp.api.views.sin_info_update").get_logger()

    logger.info('Verifying Request Method')

    if verify_method(request, ["POST"]):

        logger.info('Request Method Verified')
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
            new_description = body[SIN_FIELDS[5]]
            new_title = body[SIN_FIELDS[6]]

            # create test reviewer
                # TODO: replace with field to be added to SIN: reviewer [User]
            test_reviewer = User.objects.get(username="test_reviewer")
            test_approver = User.objects.get(username="test_approver")
            logger.info('Pulling Hard-coded Test Reviewer Profile: %s', test_reviewer.email)
            logger.info('Pulling Hard-coded Test Approver Profile: %s', test_approver.email)


            try:
                new_status = Status.objects.get(id=status_id)
                logger.info('Status Found')
                try:
                    new_user = User.objects.get(id=user_id)
                    logger.info('User Found')
                    try:

                        new_sin=Sin(id=sin_id, sin_number=sin_number, status=new_status, user=new_user,
                                        sin_title=new_title, sin_description=new_description)
                        logger.info('SIN Updated')   
                        new_sin.save()
                        
                        logger.info("Generating Email Notification For %s Status Change Request", new_status.name)
                        if new_status.id == STATUS_STATES["submitted"]:
                            logger.info('Notifying (reviewer, submitter) = (%s, %s)', test_reviewer.email, new_sin.user.email)
                            notify_reviewer(new_sin, test_reviewer)
                            confirm_submitter(new_sin, test_reviewer)
                        elif new_status.id == STATUS_STATES["reviewed"]:
                            logger.info('Notifying (reviewer, submitter) = (%s, %s)', test_reviewer.email, new_sin.user.email)
                            notify_reviewer(new_sin, test_reviewer)
                            confirm_submitter(new_sin, test_reviewer)
                            pass
                        elif new_status.id == STATUS_STATES["change"]:
                            # TODO
                            pass
                        elif new_status.id == STATUS_STATES["approved"]:
                            logger.info('Notifying (approver, submitter) = (%s, %s)', test_approver.email, new_sin.user.email)
                            notify_approver(new_sin, test_approver)
                            approve_submitter(new_sin, test_approver)
                        elif new_status.id == STATUS_STATES["denied"]:
                            # TODO
                            pass
                        elif new_status.id == STATUS_STATES["expired"]:
                            # TODO
                            pass

                        response={
                            SIN_FIELDS[1]: sin_id,
                            SIN_FIELDS[2]: sin_number,
                            SIN_FIELDS[3]: new_status.id,
                            SIN_FIELDS[4]: new_user.id,
                            SIN_FIELDS[5]: new_description,
                            SIN_FIELDS[6]: new_title
                        }
                        return JsonResponse(response, safe=False)

                    except Sin.DoesNotExist:
                        response = { 'message': 'SIN Does Not Exist'}
                        logger.info('SIN Not Found')  
                        return JsonResponse(response, status=404, safe=False)
    
                except User.DoesNotExist:
                    response = { 'message': 'User Does Not Exist'}
                    logger.info('User Not Found')
                    return JsonResponse(response, status=400, safe=False)

            except Status.DoesNotExist:
                response = { 'message' : 'Status Does Not Exist'}
                logger.info('Status Not Found')
                return JsonResponse(response, status=404, safe=False)
        
        else:
            response = { 'message' : 'Body Parameter Parsing Error'}
            logger.info('Error Parsing Parameters in Request Body')
            return JsonResponse(response, status=400, safe=False)

    else:

        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)

# GET: /api/sin?id=123456
#      /api/sin?user_email=something@gsa.gov
#      /api/sin?user_id=123
#      /api/sin?status_id=1
# POST: /api/sin 
# { body: { 
#   'sin_number': 123456,
#   'sin_title': 'title', 
#   'sin_description': 'description'
#   }
# }
# 
# Description: retrieves information for a specific SIN number or list of SIN numbers 
# for GET requests or posts a new SIN for POST requests. 
#
# GET REQUESTS
#
# GET requests can search existing SINs be any field that exists on the SIN model
# by using that field as a parameter in the query string. The available fields to
# search by are: sin_number, user_email, status_id
#
# POST REQUESTS
# 
# If the SIN being posted already exists, the POST method will attempt to update 
# an existing SIN, if its status does not prohibit it. SINs with a status of a 
# SUBMITTED, REVIEWED, APPROVED, CHANGE or DENIED will not allow updates. SINS with
# a status of EXPIRED can be overwritten and reused.
#
# In other words, POST requests that use this endpoint will only be able submit new 
# SINS, which includes old SINS that are expired and no longer in use. If you need
# to update an existing SIN with a new status or info, use the endpoint /api/updateSin.
# 
# This endpoint should only be used by submitters to submit new SINs. All reviewers
# and approvers should direct their request through the /api/updateSin endpoint.
#
# TODO: Separate POST and GET Authentication. Remove login_required Annotation and
#       manually check for authentication, so that the GET requests can be publicly
#       available and POST requests must be authenticated.
@login_required
def sin_info(request):
    
    logger = DebugLogger("sinwebapp.api.views.sin_info").get_logger()

    logger.info('Verfiying Request Method')

    if verify_method(request, ["GET", "POST"]):

        logger.info('Request Method Verified')
        # POST REQUEST: Posting new SIN to database or modifying inactive SIN
        if request.method == "POST":
            logger.info('Posting New SIN')

            if hasattr(request.user, 'email'):
                email = request.user.email
                logger.info('User Posting: %s', email)
            else:
                logger.warning('No User Associated With Incoming Request')
                return JsonResponse({ 'message': 'No User Signed In.' }, status=403)

            # TODO: if request.user.is_authenticated():
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            # TODO 1: use SIN_FIELDS array to verify body contains all parameters
            # TODO 2: use SIN_FIELDS array to pull all fields from body automatically
            # instead of doing it manually
            sin_number = body['sin_number']
            sin_title = body['sin_title']
            sin_description = body['sin_description']
            logger.info('SIN # Posting: %s', sin_number)

            # create test reviewer
                # TODO: replace with field to be added to SIN: reviewer [User]
            test_reviewer = User.objects.get(username="test_reviewer")
            logger.info('Pulling Hard-coded Test Reviewer Profile: %s', test_reviewer.email)

            # create submitted status
            new_status = Status.objects.get(id=1)
            logger.info('Status Posting: %s', new_status.name)

            # verify sin is not already active
            logger.info('Attempting To Post...')
            try: 
                sin = Sin.objects.get(sin_number=sin_number)
                logger.info('SIN # Exists!')
                if sin.status.id in [1,2,3,4]:
                    # STATUS STATES:  
                    # 1 = submitted, 2 = reviewed, 3 = change
                    # 4 = approved, 5 = denied, 6 = expired
                    logger.warning('Existing SIN Cannot Be Modified')
                    return JsonResponse({ 'Message': 'Existing SIN # Still In Process.' }, status=403)
                    
                else:
                    sin.update(user=request.user, status=new_status)
                    logger.info('Existing SIN # Updated.')
                    logger.info('Notifying (reviewer, submitter) = (%s, %s)', test_reviewer.email, sin.user.email)
                    notify_reviewer(sin, test_reviewer)
                    confirm_submitter(sin, test_reviewer)
                    return JsonResponse(sin, safe=False)
            
            # post new sin
            except Sin.DoesNotExist:
                sin = Sin.objects.create(sin_number=sin_number, user=request.user, status=new_status,
                                            sin_title=sin_title, sin_description=sin_description)
                sin.save()
                logger.info('New SIN # Posted')
                logger.info('Notifying (reviewer, submitter) = (%s, %s)', test_reviewer.email, sin.user.email)
                notify_reviewer(sin, test_reviewer)
                confirm_submitter(sin, test_reviewer)
                raw_sin = {
                    'id': sin.id,
                    'sin_number': sin.sin_number,
                    'user_id': request.user.id,
                    'status_id': new_status.id,
                    'sin_title': sin.sin_title,
                    'sin_description': sin.sin_description
                }
                return JsonResponse(raw_sin, safe=False)
                
        # GET REQUEST: retrieving information on a specific SIN, or list of SINs.
        elif request.method == "GET":
            logger.info('Retrieving SIN Info')

            if 'sin_number' in request.GET:
                sin=request.GET.get('sin_number')
                logger.info('Using ID Query Parameter: %s', sin)
                try:
                    raw_sin = Sin.objects.get(sin_number=sin)
                    retrieved_sin = {
                        'id': raw_sin.id,
                        'sin_number': raw_sin.sin_number,
                        'user_id': raw_sin.user.id,
                        'status_id': raw_sin.status.id,
                        'sin_title': raw_sin.sin_title,
                        'sin_description': raw_sin.sin_description
                    }
                    logger.info('SIN Found!')
                    return JsonResponse(retrieved_sin, safe=False)

                except Sin.DoesNotExist:
                    retrieved_sin = { 'message': 'SIN Does Not Exist' }
                    logger.warning('SIN Not Found!')
                    return JsonResponse(retrieved_sin, status=404, safe=False)

            elif 'user_email' in request.GET:
                user_email = request.GET.get('user_email')
                logger.info('Using User Email Query Parameter: %s', user_email)
                try:
                    search_user = User.objects.get(email=user_email)
                    logger.info('User Found!')
                    retrieved_sin = list(Sin.objects.filter(user=search_user).values())
                    return JsonResponse(retrieved_sin, safe=False)

                except User.DoesNotExist:
                    retrieved_sin = { 'message': 'User Does Not Exist'}
                    logger.warning('User Not Found!')
                    return JsonResponse(retrieved_sin, status=404, safe=False)


            elif 'user_id' in request.GET:
                user_id = request.GET.get('user_id')
                logger.info('Using User Id Query Parameter: %s', user_id)
                try:
                    search_user = User.objects.get(id=user_id)
                    logger.info('User Found!')
                    retrieved_sin = list(Sin.objects.filter(user=search_user).values())
                    return JsonResponse(retrieved_sin, safe=False)

                except User.DoesNotExist:
                    retrieved_sin = {'message': 'User Does Not Exist'}
                    logger.warning('User Not Found!')
                    return JsonResponse(retrieved_sin, status=404, safe=False)


            elif 'status_id' in request.GET:
                status_id = request.GET.get('status_id') 
                logger.info('Using Status Query Parameter: %s', status_id)

                try:  
                    search_status = Status.objects.get(id=status_id)
                    logger.info('Status Found!')
                    retrieved_sin = list(Sin.objects.filter(status=search_status).values()) 
                    return JsonResponse(retrieved_sin, safe=False)

                except User.DoesNotExist:
                    retrieved_sin = { 'message': 'Status Does Not Exist' }
                    logger.warning('Status Not Found!')
                    return JsonResponse(retrieved_sin, status=404, safe=False)

            else:
                retrieved_sin ={ 'message': 'No Query Parameters Provided' }
                logger.info('No Query Parameters Provided')
                return JsonResponse(retrieved_sin, status=400, safe=False)
        
    else:

        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)

# GET: /api/sins
#
# Description: retrieves information on all SIN numbers
@login_required
def sin_info_all(request):
    logger = DebugLogger("sinwebapp.api.views.sins_info_all").get_logger()

    logger.info('Verifying Request Method')

    if verify_method(request, ["GET"]):
        logger.info('Request Method Verified')
        logger.info('Retrieving All SIN Info')

        try:
            retrieved_sins = list(Sin.objects.values())
            if len(retrieved_sins) == 0:
                retrieved_sins = { 'message': '0 SINs found' }
                logger.info('0 SINs Found!')
                return JsonResponse(retrieved_sins, status=404, safe=False)

            else:
                logger.info('SINs Found!')
                return JsonResponse(retrieved_sins, safe=False)

        except Sin.DoesNotExist:
            retrieved_sins = { 'message': 'SINs Do Not Exist' }
            logger.info('SINs Not Found!')
            return JsonResponse(retrieved_sins, status=404, safe=False)
    else:

        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)


# GET: /api/status?id=1
# 
# Description: retrieves information for a specific Status
@login_required
def status_info(request):
    logger = DebugLogger("sinwebapp.api.views.status_info").get_logger()

    logger.info('Verifying Request Method')

    if verify_method(request, ["GET"]):

        logger.info('Request Method Verified')
        logger.info('Retrieving Status Info')

        if 'id' in request.GET:
            status_id=request.GET.get('id')
            logger.info('Using Status Id Query Parameter: %s', status_id)
            try:
                raw_status = Status.objects.get(id=status_id)
                retrieved_status = {
                    'id': raw_status.id,
                    'name' : raw_status.name,
                    'description': raw_status.description,
                }
                logger.info('Status Found!')
                return JsonResponse(retrieved_status, safe=False)

            except Status.DoesNotExist:
                retrieved_status = { 'message': 'Status Does Not Exist' }
                logger.info('Status Not Found!')
                return JsonResponse(retrieved_status, status=404, safe=False)

        else:
            retrieved_status = { 'message': 'Input Error' }
            logger.info('Parameter Not Provided')
            return JsonResponse(retrieved_status, status=400, safe=False)

    else:

        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)

# GET: /api/statuses
#
# Description: Retrieves a list of all Statuses accessible by the user
# signed into the request's session
@login_required
def user_status_info(request):
    logger = DebugLogger('sinwebapp.api.views.user_status_info').get_logger()

    logger.info('Verifying Request Method')

    if verify_method(request, ["GET"]):
        logger.info('Request Method Verified')
        logger.info('Retrieving All Statuses')

        try:
            group_list = request.user.groups.values_list('name', flat=True)
            if GROUPS['submitter'] in group_list:
                retrieved_statuses = list(Status.objects.filter(id__in=[STATUS_STATES['submitted'],
                                                                        STATUS_STATES['terminating']]).values())
                logger.info('Status Found!')
                return JsonResponse(retrieved_statuses, safe=False)

            elif GROUPS['reviewer'] in group_list:
                retrieved_statuses = list(Status.objects.filter(id__in=[STATUS_STATES['submitted'],
                                                                        STATUS_STATES['reviewed'],
                                                                        STATUS_STATES['change']]).values())
                logger.info('Statuses Found!')
                return JsonResponse(retrieved_statuses, safe=False)

            elif GROUPS['approver'] in group_list or GROUPS['admin'] in group_list:
                retrieved_statuses = list(Status.objects.values())
                logger.info('Statuses Found!')
                return JsonResponse(retrieved_statuses, safe=False)

            else:
                retreived_statuses = { 'message' : 'User Does Not Have Any Permissions'}
                logger.info('User Has No Permissions!')
                return JsonResponse(retrieved_statuses, status=403, safe=False)


        except Status.DoesNotExist:
            retrieved_statuses = {'message': 'Statuses Do Not Exist'}
            logger.info('Statuses Not Found!')
            return JsonResponse(retrieved_statuses, status=404, safe=False)

    else:

        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)

        
@login_required
def status_info_all(request):
    logger = DebugLogger('sinwebapp.api.views.status_info_all').get_logger()
    logger.info('Verifying Request Method')

    if verify_method(request, ["GET"]):

        logger.info('Request Method Verified')
        logger.info('Retrieving All Statuses')

        try:
            group_list = request.user.groups.values_list('name', flat=True)
            retrieved_statuses = list(Status.objects.values())

            if len(retrieved_statuses)==0:
                retrieved_statues = { 'message' : '0 Statuses Found' }
                logger.info('0 Statuses Found!')
                return JsonResponse(retrieved_statuses, status=404, safe=False)
                
            else:
                logger.info('Statuses Found!')
                return JsonResponse(retrieved_statuses, safe=False)

        except Status.DoesNotExist:
            retrieved_statuses = {'message': 'Statuses Do Not Exist'}
            logger.info('Statuses Not Found!')
            return JsonResponse(retrieved_statuses, status=404, safe=False)
    
    else: 
        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)