from debug import DebugLogger
from api.models import Status, STATUS_STATES

def init_status(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_status").get_logger()

    key_list = list(STATUS_STATES.keys()) 
    val_list = list(STATUS_STATES.values()) 
    submitted = Status.objects.get_or_create(name=key_list[val_list.index(1)], 
                                             description="SIN form has been submitted for review and approval.")
    reviewed = Status.objects.get_or_create(name=key_list[val_list.index(2)], 
                                             description="SIN form has been reviewed and is ready for approval.")
    change = Status.objects.get_or_create(name=key_list[val_list.index(3)], 
                                             description="SIN form requires change before approval.")
    approved = Status.objects.get_or_create(name=key_list[val_list.index(4)], 
                                            description="SIN form has been approved.")
    denied = Status.objects.get_or_create(name=key_list[val_list.index(5)], 
                                             description="SIN form has been denied.")
    expired = Status.objects.get_or_create(name=key_list[val_list.index(6)],
                                             description="SIN form has expired.")