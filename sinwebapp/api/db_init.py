import csv, os
from debug import DebugLogger
from random import randint
from django.contrib.auth.models import User
from api.models import Status, Sin, SinData, STATUS_STATES
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
    logger.info("Initializing SinData")

    filepath = BASE_DIR+'/db/sin_data.csv'
    logger.info('Opening CSV Located at: %s', filepath)

    with open(filepath) as f:
        reader = csv.reader(f)
        next(reader)
        count=1
        modulo = randint(70, 120)
        logger.info("Randomizing Debug Output Because Why Not")
        for row in reader:
            created = SinData.objects.get_or_create(
                sin_number=row[0], schedule_number=row[1], special_item_number=row[2],
                sin_group_title=row[3], sin_description1=row[4], sin_description2=row[5],
                sin_order=row[6], co_fname=row[7], co_lname=row[8], co_phone=row[9],
                co_email=row[10]
            )
            count+=1
            if count%modulo == 0:
                logger.info(" INSERTION # %s : (sin_number, sin_description1) = (%s, %s) ", count, row[0], row[4][0:50])

def populate_sins(app, schema_editor):
    logger = DebugLogger("api.db_init.populate_sins").get_logger()
    logger.info("Populating Sin Table With Raw SinData")

    super_email = os.getenv('DJANGO_SUPERUSER_EMAIL')
    super_user = User.objects.get(email=super_email)

    expired_status = Status.objects.get(id=STATUS_STATES['expired'])

    raw_data = list(SinData.objects.values())

    logger.info("Randomizing Debug Output Because Why Not")
    count = 1
    modulo = randint(70,120)
    for sin in raw_data:
        # clean and parse data
        # remove trailing spaces
        if count%modulo == 0:
            logger.info('Processing SinData Table Entry # %s', sin['id'])
        this_raw_sin = SinData.objects.get(id=sin['id'])
        try:
            if sin['sin_number']:
                try:
                    if sin['sin_group_title']:
                        try:
                            if sin['sin_description1']:
                                Sin.objects.get_or_create(user=super_user, status=expired_status, sin_map=this_raw_sin,
                                                            sin_number=sin['sin_number'], sin_group_title=sin['sin_group_title'], 
                                                            sin_description1=sin['sin_description1'])
                                if count%modulo == 0:
                                    logger.info('SinDate Table Entry # %s Validated', sin['id'])
                                    logger.info('Passing SinData Table Entry # %s To Sin Table', sin['id'])
                            else:
                                if count%modulo == 0:
                                    logger.info('Null "sin_description1" Field For Entry %s', sin['id'])
                                    logger.warn('Preventing Insertion Into Sin Table')
                        except NameError:
                            if count%modulo == 0:
                                logger.info('Undefined "sin_description1" field for entry # %s', sin['id'])
                                logger.warn('Preventing Insertion Into Sin Table')
                    else:
                        if count%modulo == 0:
                            logger.info('Null "sin_group_title" Field For Entry %s', sin['id'])
                            logger.warn('Preventing Insertion Into Sin Table')
                except NameError:
                    if count%modulo == 0:
                        logger.info('Undefined "sin_group_title" field for entry # %s', sin['id'])
                        logger.warn('Preventing Insertion Into Sin Table')

            else:
                if count%modulo == 0:
                    logger.info('Null "sin_number" Field For Entry %s', sin['id'])
                    logger.warn('Preventing Insertion Into Sin Table')
        except NameError:
            if count%modulo == 0:
                logger.info('Undefined "sin_number" field for entry # %s', sin['id'])
                logger.warn('Preventing Insertion Into Sin Table')
        count+=1

