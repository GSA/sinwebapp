from django.http import JsonResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from api.models import Sin, Status
from api.models import STATUS_STATES, SIN_FIELDS
from authentication.db_init import GROUPS
from debug import DebugLogger


def search(request):
    logger = DebugLogger("sinwebapp.api.views.user_info").get_logger()
    logger.info('Verifying Request Method')
    

    if request.method == "GET":
        logger.info('Request Method Verified')
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
                metadata = {
                    'count': 0
                }
                response = {
                    'metadata': metadata,
                    'records' : retrieved_sin
                }
                logger.info('SIN Found!')
                return JsonResponse(response, safe=False)

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
                metadata = {
                    'count': 0
                }
                response = {
                    'metadata': metadata,
                    'records' : retrieved_sin
                }
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
                metadata = {
                    'count': 0
                }
                response = {
                    'metadata': metadata,
                    'records' : retrieved_sin
                }
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
                metadata = {
                    'count': 0
                }
                response = {
                    'metadata': metadata,
                    'records' : retrieved_sin
                } 
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

def sins(request):
    pass