from django.contrib import admin
from django.contrib.auth.models import Group
from .db_config import GroupAdminForm 
from debug import DebugLogger

logger = DebugLogger("admin.py").get_logger()

# Create a new Group admin.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']
    
# Unregister the original Group admin.
# admin.site.unregister(Group)
# Register the new Group ModelAdmin.
# admin.site.register(Group, GroupAdmin)