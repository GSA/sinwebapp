from django.contrib import admin
from django.contrib.auth.models import Group
from authentication.db_config import GroupAdmin

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)