from debug import DebugLogger
from api.models import Status, STATUS_STATES

def init_status(apps, schema_editor):
    logger = DebugLogger("api.db_init.init_status").get_logger()
    logger.info('Initializing Status Types')
    
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

# import csv
import csv
from api.models import SinData
def init_sindata(app, schema_editor):
    logger = DebugLogger("api.db_init.init_sindata").get_logger()
    logger.info("Initializing Sin data")

#     Sin = ContentType.objects.get_for_model(Sin)
#     sin_number = Sin.objects.get_or_create(name=row[0], content_type=sin, codename='sin_number')
#     schedule_number = Sin.objects.get_or_create(name=row[1], content_type=sin, codename='schedule_number')
#     special_item_number = Sin.objects.get_or_create(name=row[2], content_type=sin, codename='special_item_number')
#     sin_group_title = Sin.objects.get_or_create(name=row[3], content_type=sin, codename='sin_group_title')
#     sin_description1 = Sin.objects.get_or_create(name=row[4], content_type=sin, codename='sin_description1')
#     sin_description2 = Sin.objects.get_or_create(name=row[5], content_type=sin, codename='sin_description2')
#     sin_order = Sin.objects.get_or_create(name=row[6], content_type=sin, codename='sin_order')
#     co_fname = Sin.objects.get_or_create(name=row[7], content_type=sin, codename='co_fname')
#     co_lname = Sin.objects.get_or_create(name=row[8], content_type=sin, codename='co_lname')
#     co_phone = Sin.objects.get_or_create(name=row[9], content_type=sin, codename='co_phone')
#     co_email = Sin.objects.get_or_create(name=row[10], content_type=sin, codename='co_email')


    # import data loop thru the objects
    # Skip first row
    # def import_data():
    with open('../db/sin_data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            next(reader, None) 
            created = SinData.objects.get_or_create(
                  sin_number=row[0],
                  schedule_number=row[1],
                  special_item_number=row[2],
                  sin_group_title=row[3],
                  sin_description1=row[4],
                  sin_description2=row[5],
                  sin_order=row[6],
                  co_fname=row[7],
                  co_lname=row[8],
                  co_phone=row[9],
                  co_email=row[10]
                )
            logger.info("Sin Created: %s", created.co_email)


