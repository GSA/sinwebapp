from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from debug import DebugLogger


def init_groups(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_groups").get_logger()
    logger.info("> Initializing Groups...")

    admin_user_group = Group.objects.get_or_create(name='admin_user_group')
    read_only_group = Group.objects.get_or_create(name='read_only_group')
    submitter_group = Group.objects.get_or_create(name='submitter_group')
    reviewer_group = Group.objects.get_or_create(name='reviewer_group')
    approver_group = Group.objects.get_or_create(name='approver_group')

def init_permissions(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_permissions").get_logger()
    logger.info("> Initializing Permissions...")

    ct = ContentType.objects.get_for_model(User)

    admin_sin = Permission.objects.get_or_create(name='Can administer SIN', content_type=ct, codename='admin_sin')
    read_sin = Permission.objects.get_or_create(name='Can read SIN', content_type=ct, codename='read_sin')
    submit_sin = Permission.objects.get_or_create(name='Can submit SIN', content_type=ct, codename='submit_sin')
    review_sin = Permission.objects.get_or_create(name='Can review SIN', content_type=ct, codename='review_sin')
    approve_sin = Permission.objects.get_or_create(name='Can approve SIN', content_type=ct, codename='approve_sin')

def init_users(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_users").get_logger()
    logger.info("> Initializing Sample Users...")

        # name,email,pass @TODO change to actual email addresses that can be tested
    read_only_user = User.objects.create_user('read_only_user', 'read_only_user@gsa.gov', 'read_only_user')
    read_only_group = Group.objects.get(name='read_only_group')
    read_only_group.user_set.add(read_only_user)

    submitter_user = User.objects.create_user('submitter_user', 'submitter_user@gsa.gov', 'submitter_user')
    submitter_group = Group.objects.get(name='submitter_group')
    submitter_group.user_set.add(submitter_user)

    reviewer_user = User.objects.create_user('reviewer_user', 'reviewer_user@gsa.gov', 'reviewer_user')
    reviewer_group = Group.objects.get(name='reviewer_group')
    reviewer_group.user_set.add(reviewer_user)

    approver_user = User.objects.create_user('approver_user', 'approver_user@gsa.gov', 'approver_user')
    approver_group = Group.objects.get(name='approver_group')
    approver_group.user_set.add(approver_user)

def init_group_permissions(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_group_permissions").get_logger()
    logger.info("> Initializing Group Permissions...")

    read_only_group = Group.objects.get(name='read_only_group')
    read_only_permissions = Permission.objects.get(codename='read_sin')
    read_only_group.permissions.add(read_only_permissions)

    submitter_group = Group.objects.get(name='submitter_group')
    submitter_permissions = Permission.objects.get(codename='submit_sin')
    submitter_group.permissions.add(submitter_permissions)

    reviewer_group = Group.objects.get(name='reviewer_group')
    reviewer_permissions = Permission.objects.get(codename='review_sin')
    reviewer_group.permissions.add(reviewer_permissions)

    approver_group = Group.objects.get(name='approver_group')
    approver_permissions = Permission.objects.get(codename='approve_sin')
    approver_group.permissions.add(approver_permissions)