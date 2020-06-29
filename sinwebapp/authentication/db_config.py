
from django.contrib.auth.models import Group, User, Permission

def init_groups():

#read_only
group, created = Group.objects.get_or_create(name='read_only')
if created:
group.permissions.add(can_read_sin)
logger.info('read_only Group created')

#submitter
group, created = Group.objects.get_or_create(name='submitter')
if created:
group.permissions.add(can_edit_sin)
logger.info('Submitter Group created')

#reviewer
group, created = Group.objects.get_or_create(name='reviewer')
if created:
group.permissions.add(can_edit_sin)
logger.info('Reviewer Group created')

#approver
group, created = Group.objects.get_or_create(name='approver')
if created:
group.permissions.add(can_edit_sin)
logger.info('Approver Group created')

#admin
group, created = Group.objects.get_or_create(name='admin_user')
if created:
group.permissions.add(can_edit_sin, can_edit_users)
logger.info('Admin Group created')

def init_permissions():

User = apps.get_model('auth', 'User')
Permission = apps.get_model('auth', 'Permission')
db_alias = schema_editor.connection.alias
Permission.objects.using(db_alias).bulk_create([
Permission(codename='can_read_sin', name='Can view SIN data'),
Permission(codename='can_edit_sin', name='Can edit SIN data'),
Permission(codename='can_edit_users', name='Can edit Users')
])

def init_users():

# create users here
pass

class Migration(migrations.Migration):

dependencies = [
('sinwebapp', '0001_initial'),
]

operations = [
migrations.RunPython(add_group_permissions),
]
