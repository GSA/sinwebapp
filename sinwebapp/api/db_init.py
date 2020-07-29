from debug import DebugLogger
from api.models import Status

def init_status(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_groups").get_logger()

    submitted = Status.objects.get_or_create(status='submitted', 
                                             description="SIN form has been submitted for review and approval.")
    reviewed = Status.objects.get_or_create(status='reviewed', 
                                             description="SIN form has been reviewed and is ready for approval.")
    change = Status.objects.get_or_create(status='change', 
                                             description="SIN form requires change before approval.")
    approved = Status.objects.get_or_create(status='approved', 
                                            description="SIN form has been approved.")
    denied = Status.objects.get_or_create(status='denied', 
                                             description="SIN form has been denied.")