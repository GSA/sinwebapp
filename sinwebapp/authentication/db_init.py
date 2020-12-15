from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from core import settings
from debug import DebugLogger
import os, sys

GROUPS = {
    'submitter':'submitter_group', 
    'reviewer': 'reviewer_group', 
    'approver': 'approver_group', 
    'admin': 'admin_group',
    'portfolio': 'portfolio_group', 
    'steward': 'steward_group',
    'pmo_approver': 'pmo_appover_group', 
    'opc_approver': 'opc_approver_group',
    'system_approver': 'system_approver_group'
}

def init_groups(apps, schema_editor):
    logger = DebugLogger("authentication.db_init.init_groups").get_logger()
    logger.info("Initializing Groups")

    admin_group = Group.objects.get_or_create(name=GROUPS['admin'])
    submitter_group = Group.objects.get_or_create(name=GROUPS['submitter'])
    reviewer_group = Group.objects.get_or_create(name=GROUPS['reviewer'])
    approver_group = Group.objects.get_or_create(name=GROUPS['approver'])
    portfolio_group = Group.objects.get_or_create(name=GROUPS['portfolio'])
    steward_group = Group.objects.get_or_create(name=GROUPS['pmo_approver'])
    pmo_appover = Group.objects.get_or_create(name=GROUPS['opc_approver'])
    system_approver = Group.objects.get_or_create(name=GROUPS['system_approver'])    

def init_permissions(apps, schema_editor):
    logger = DebugLogger("authentication.db_init.init_permissions").get_logger()
    logger.info("Initializing Permissions")

    ct = ContentType.objects.get_for_model(User)
    submit_sin = Permission.objects.get_or_create(name='Submit SIN', content_type=ct, codename='submit_sin')
    review_sin = Permission.objects.get_or_create(name='Review SIN', content_type=ct, codename='review_sin')
    approve_sin = Permission.objects.get_or_create(name='Approve SIN', content_type=ct, codename='approve_sin')

def init_group_permissions(apps, schema_editor):
    logger = DebugLogger("authentication.db_init.init_group_permissions").get_logger()
    logger.info("Initializing Group Permissions")
    
    submitter_group = Group.objects.get(name=GROUPS['submitter'])
    submitter_permissions = Permission.objects.get(codename='submit_sin')
    submitter_group.permissions.add(submitter_permissions)

    reviewer_group = Group.objects.get(name=GROUPS['reviewer'])
    reviewer_permissions = Permission.objects.get(codename='review_sin')
    reviewer_group.permissions.add(reviewer_permissions)

    approver_group = Group.objects.get(name=GROUPS['approver'])
    approver_permissions = Permission.objects.get(codename='approve_sin')
    approver_group.permissions.add(approver_permissions)

    admin_group = Group.objects.get(name=GROUPS['admin'])
    admin_group.permissions.add(submitter_permissions)
    admin_group.permissions.add(reviewer_permissions)
    admin_group.permissions.add(approver_permissions)

def init_default_users(app, schema_editor):
    logger = DebugLogger("authentication.db_init.init_default_users").get_logger()
    logger.info("Initializing Default Users")

    if settings.APP_ENV == 'local' or settings.APP_ENV == 'container':
        logger.info("Creating Users For Local Deployment")

        submitter = User.objects.create_user(username="submitter", email="submitter@gsa.gov")
        submitter_group = Group.objects.get(name=GROUPS['submitter'])
        submitter_group.user_set.add(submitter)
        submitter.save()

        approver = User.objects.create_user(username="approver", email="approver@gsa.gov")
        approver_group = Group.objects.get(name=GROUPS['approver'])
        approver_group.user_set.add(approver)
        approver.save()
        
        reviewer = User.objects.create_user(username="reviewer",email="reviewer@gsa.gov")
        reviewer_group = Group.objects.get(name=GROUPS['reviewer'])
        reviewer_group.user_set.add(reviewer)
        reviewer.save()

    logger.info("Creating Test Reviewer")
    try:
        test_reviewer = User.objects.create_user(username="test_reviewer", email="theodros.desta@gsa.gov", password="root")
        reviewer_group = Group.objects.get(name=GROUPS['reviewer'])
        reviewer_group.user_set.add(test_reviewer)
        test_reviewer.save()
    except: 
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.error("Error Occurred Creating Test Reviewer : %s, \n :%s \n :%s \n", e, f, g)

    logger.info("Creating Test Approver")
    try:
        test_approver= User.objects.create_user(username="test_approver", email="tina.burns@gsa.gov", password="root")
        approver_group = Group.objects.get(name=GROUPS['approver'])
        approver_group.user_set.add(test_approver)
        test_approver.save()
    except:
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.error("Error Occurred Creating Test Approver: %s, \n :%s \n :%s \n", e, f, g)

    logger.info("Creating Super-User Using Environment Variables")
    try:
        super_user = User.objects.create_superuser(username=os.getenv('DJANGO_SUPERUSER_USERNAME'), 
                                                    email=os.getenv('DJANGO_SUPERUSER_EMAIL'), 
                                                    password=os.getenv('DJANGO_SUPERUSER_PASSWORD'))
        admin_group = Group.objects.get(name=GROUPS['admin'])
        admin_group.user_set.add(super_user)
        super_user.save()
    except:
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.error("Error Occurred Creating Super User: %s, \n :%s \n :%s \n", e, f, g)