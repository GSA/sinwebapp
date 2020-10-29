from django.http import JsonResponse
from django.contrib.auth.models import Group, User

from api.models import Sin, Status
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
                    'count': 1
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
                    'count': len(retrieved_sin)
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
                    'count': len(retrieved_sin)
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
                    'count': len(retrieved_sin)
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
    logger = DebugLogger("sinwebapp.api.views.sins_info_all").get_logger()
    logger.info('Verifying Request Method')

    if request.method == "GET":
        logger.info('Request Method Verified')
        logger.info('Retrieving All SIN Info')

        try:
            retrieved_sins = list(Sin.objects.values())
            metadata = {
                    'count': len(retrieved_sins)
            }
            response = {
                'metadata': metadata,
                'records': retrieved_sins
            }
            logger.info('SINs Found!')
            return JsonResponse(retrieved_sins, safe=False)

        except Sin.DoesNotExist:
            retrieved_sins = { 'message': 'SINs Not Found' }
            logger.info('SINs Not Found!')
            return JsonResponse(retrieved_sins, status=404, safe=False)
    else:

        logger.info('Request Method Rejected')
        response = { 'message' : "Method Not Allowed" }
        return JsonResponse(response, status=405, safe=False)

def status(request):
    logger = DebugLogger('sinwebapp.api.views_public.status').get_logger()
    logger.info('Verifying Request Method')

    if request.method == "GET":

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