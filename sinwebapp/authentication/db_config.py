from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from debug import DebugLogger


def init_groups(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_groups").get_logger()
    logger.info("-------------------------------------------------")
    logger.info("Initializing Groups...")

    admin_user = Group.objects.get_or_create(name='admin_user')
    read_only = Group.objects.get_or_create(name='read_only')
    submitter = Group.objects.get_or_create(name='submitter')
    reviewer = Group.objects.get_or_create(name='reviewer')
    approver = Group.objects.get_or_create(name='approver')

def init_permissions(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_permissions").get_logger()
    logger.info("-------------------------------------------------")
    logger.info("Initializing Permissions...")

    ct = ContentType.objects.get_for_model(User)
    read_sin = Permission.objects.get_or_create(name="Can read SIN", content_type=ct, codename="read_sin")
    edit_sin = Permission.objects.get_or_create(name="Can edit SIN", content_type=ct, codename="edit_sin")
    approve_sin = Permission.objects.get_or_create(name="Can approve SIN", content_type=ct, codename="approve_sin")


def init_users(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_users").get_logger()
    logger.info("-------------------------------------------------")
    logger.info("Initializing Users...")

    # name,email,pass
    read_only_user = User.objects.create_user('read_only_user', 'read_only_user@gsa.gov', 'read_only_user')
    submitter_user = User.objects.create_user('submitter_user', 'submitter_user@gsa.gov', 'submitter_user')
    reviewer_user = User.objects.create_user('reviewer_user', 'reviewer_user@gsa.gov', 'reviewer_user')
    approver_user = User.objects.create_user('approver_user', 'approver_user@gsa.gov', 'approver_user')