from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from debug import DebugLogger


def login_page(request):
    return render(request, 'login_splash.html')

@login_required
def login_success_page(request):
    logger = DebugLogger("sinwebapp.authentication.views.login_success_page").get_logger()
    logger.info('Accessing Login Page...')
    if (not hasattr(request.user, 'groups')) or (not request.user.groups.filter(name__in=['reviewer_group', 
                                                                                            'submitter_group',
                                                                                            'approver_group',
                                                                                            'admin_group']).exists()):
        logger.warn('User Has No Group, Assigning Default Group submitter_group')
        approver_group = Group.objects.get(name='submitter_group')
        user_object = User.objects.get(email=request.user.email)
        approver_group.user_set.add(user_object)
    return render(request, 'login_success.html')
    
def logout_page(request):
    logout(request)
    return render(request, 'logout_splash.html')
