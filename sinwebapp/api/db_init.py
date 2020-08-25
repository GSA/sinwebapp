import csv
from debug import DebugLogger
from api.models import Status, SinData, STATUS_STATES
from core.settings import BASE_DIR

def init_status(apps, schema_editor):
    logger = DebugLogger("api.db_init.init_status").get_logger()
    logger.info('Initializing Status Types')
    
    key_list = list(STATUS_STATES.keys()) 
    val_list = list(STATUS_STATES.values()) 
    
    submitted = Status.objects.get_or_create(id = 1, name=key_list[val_list.index(1)], 
                                             description="SIN form has been submitted for review and approval.")
    reviewed = Status.objects.get_or_create(id = 2, name=key_list[val_list.index(2)], 
                                             description="SIN form has been reviewed and is ready for approval.")
    change = Status.objects.get_or_create(id = 3, name=key_list[val_list.index(3)], 
                                             description="SIN form requires change before approval.")
    approved = Status.objects.get_or_create(id = 4, name=key_list[val_list.index(4)], 
                                            description="SIN form has been approved.")
    denied = Status.objects.get_or_create(id = 5, name=key_list[val_list.index(5)], 
                                             description="SIN form has been denied.")
    expired = Status.objects.get_or_create(id = 6, name=key_list[val_list.index(6)],
                                             description="SIN form has expired.")

def init_sindata(app, schema_editor):
    logger = DebugLogger("api.db_init.init_sindata").get_logger()
    logger.info("Initializing SIN data")

    # import data loop thru the objects
    # Skip first row
    # def import_data():
    filepath = BASE_DIR+'/db/sin_data.csv'
    logger.info('Opening CSV Located at: %s', filepath)
    with open(filepath) as f:
        reader = csv.reader(f)
        next(reader)
        count=0
        for row in reader:
            created = SinData.objects.get_or_create(
                sin_number=row[0], schedule_number=row[1], special_item_number=row[2],
                sin_group_title=row[3], sin_description1=row[4], sin_description2=row[5],
                sin_order=row[6], co_fname=row[7], co_lname=row[8], co_phone=row[9],
                co_email=row[10]
            )
            count+=1
            logger.info(" INSERTION # %s : (sin_number, sin_group_title) = (%s, %s) ", count, row[0], row[3])
