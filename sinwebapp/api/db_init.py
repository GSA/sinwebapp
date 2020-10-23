import csv, os, sys
from debug import DebugLogger
from random import randint
from django.contrib.auth.models import User
from api.models import Status, Sin, SinData, STATUS_STATES
from core.settings import BASE_DIR

DB_LIMIT=21

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
    terminating = Status.objects.get_or_create(id = 7, name=key_list[val_list.index(7)],
                                             description="SIN form has been submitted for termination")
    terminated = Status.objects.get_or_create(id=8, name=key_list[val_list.index(8)],
                                             description="SIN from has been terminated")

def init_sindata(app, schema_editor):
    logger = DebugLogger("api.db_init.init_sindata").get_logger()
    logger.info("Initializing SinData")

    filepath = BASE_DIR+'/db/mas_sin_attributes.csv'
    logger.info('Opening CSV Located at: %s', filepath)

    with open(filepath) as f:
        reader = csv.reader(f)
        next(reader)
        count=1
        modulo = randint(70, 120)
        logger.info("Randomizing Debug Output Because Why Not")
        for row in reader:
            try:
                state_flag = True if row[5] == 'Y' else False
                set_flag = True if row[6] == 'Y' else False
                t_flag = True if row[9] == 'Y' else False
                o_flag = True if row[10] == 'Y' else False
                end = row[4] if 'NULL' not in row[4] else None
                created = SinData.objects.get_or_create(
                    sin_number=row[0], sin_title=row[1], sin_description=row[2], 
                    begin_date=row[3], end_date=end, state_and_local=state_flag,
                    set_aside=set_flag, service_comm_code=row[7], 
                    tdr_flag=t_flag, olm_flag=o_flag, max_order_limit=row[11]
                )
                count+=1
                if count%modulo == 0:
                    logger.info(" INSERTION # %s : (sin_number, sin_title) = (%s, %s) ", count, row[0], row[1][0:50])
            except:
                e = sys.exc_info()[0]
                f = sys.exc_info()[1]
                g = sys.exc_info()[2]
                logger.warn('Error Occured For (sin_number, sin_title, description): (%s, %s, %s)', 
                                row[0], row[1], row[2])
                logger.error("Error Occurred Proccessing SINData: %s, \n :%s \n :%s \n", e, f, g)
                logger.warn('Preventing Insertion Into SINData Table')

def populate_sins(app, schema_editor):
    logger = DebugLogger("api.db_init.populate_sins").get_logger()
    logger.info("Populating Sin Table With Raw SinData")

    logger.info('Retrieving Super User With Email: %s', os.getenv('DJANGO_SUPERUSER_EMAIL'))
    try:
        super_user = User.objects.get(email=os.getenv('DJANGO_SUPERUSER_EMAIL'))
    except:
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.error("Error Occurred Retrieving Super User: %s, \n :%s \n :%s \n", e, f, g)

    expired_status = Status.objects.get(id=STATUS_STATES['expired'])

    raw_data = list(SinData.objects.values())

    logger.info("Randomizing Debug Output Because Why Not")
    count = 1
    modulo = randint(10,DB_LIMIT)
    for sin in raw_data:
        # TODO: clean and parse data
        # TODO: remove trailing spaces

        this_raw_sin = SinData.objects.get(id=sin['id'])
        try:
            # Hard Code Data Limit To 21 for POC
            if sin['sin_number'] and sin['sin_title'] and count<DB_LIMIT:
                if count%modulo == 0:
                    logger.info('Processing SinData Table Entry # %s', sin['id'])

                Sin.objects.get_or_create(user=super_user, status=expired_status, sin_map=this_raw_sin,
                                            sin_number=sin['sin_number'], sin_title=sin['sin_title'], 
                                            sin_description=sin['sin_description'])
                if count%modulo == 0:
                    logger.info('SinData Table Entry # %s Validated', sin['sin_number'])
                    logger.info('Passing SinData Table Entry # %s To Sin Table', sin['sin_number'])
    
        except:
            e = sys.exc_info()[0]
            f = sys.exc_info()[1]
            g = sys.exc_info()[2]
            logger.warn('Error Occured For Entry #%s (sin_number, sin_title, description): (%s, %s, %s)', 
                            sin['id'], sin['sin_number'], sin['sin_title'],['sin_description'])
            logger.error("Error Occurred Proccessing SIN: %s, \n :%s \n :%s \n", e, f, g)
            logger.warn('Preventing Insertion Into SIN Table')
            
        count+=1

