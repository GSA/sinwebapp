from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType

import logging

logger = logging.getLogger(__name__)

def init_groups(apps, schema_editor):
    # admin_user
    admin_user, created = Group.objects.get_or_create(name='admin_user')
    if created:
        logger.info('Admin Group created')

    # read_only
    read_only, created = Group.objects.get_or_create(name='read_only')
    if created:
        logger.info('read_only Group created')

    #submitter
    submitter, created = Group.objects.get_or_create(name='submitter')
    if created:
        logger.info('Submitter Group created')

    #reviewer
    reviewer, created = Group.objects.get_or_create(name='reviewer')
    if created:
        logger.info('Reviewer Group created')

    #approver
    approver, created = Group.objects.get_or_create(name='approver')
    if created:
        logger.info('Approver Group created')

def init_permissions(apps, schema_editor):
    pass

def init_users(apps, schema_editor):

    # create users here
    pass
