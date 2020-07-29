from debug import DebugLogger
from api.models import Status

def init_status(apps, schema_editor):
    logger = DebugLogger("authentication.db_config.init_groups").get_logger()

    submitted = Status(status="submitted", description="SIN form has been submitted.")
    reviewed = Status(status="reviewed", description="SIN form has been reviewed.")
    change = Status(status='change', description="SIN form requires change before approval")
    approved = Status(status='approved', description="SIN form has been approved.")
    denied = Status(status='denied', description="SIN form has been denied.")