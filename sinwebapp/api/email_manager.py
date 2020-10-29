from django.core.mail import send_mail
from core import settings
from datetime import datetime
from debug import DebugLogger
from core import settings
import os, sys, json

def get_template():
    template_file = os.path.join(settings.BASE_DIR, 'api', 'email_templates',"email_templates.json")
    with open(template_file) as f:
        template = json.load(f)
    return template

    # TODO: replace second argument with new field on SIN: reviewer [user]
def confirm_submitter(sin, reviewer):
    logger = DebugLogger("sinwebapp.api.email_manager.confirm_submitter").get_logger()

    logger.info('Confirming SIN # %s Submission Status %s For: %s To Reviewer: %s', 
                    sin.sin_number, sin.status.name, sin.user.email, reviewer.email )
    
    message_body = get_template()['submitter_confirm']['body']
    message_body = message_body.format(CHANGE_REQUEST_TYPE=sin.status.name, SIN=sin.sin_number, 
                                        DATE=datetime.now(), REVIEWER_EMAIL=reviewer.email, 
                                        SUBMITTED_NAME=sin.user.username, SUBMITTER_EMAIL=sin.user.email)
    logger.info('Email Body: %s', message_body)

    try:
        send_mail(subject=get_template()['submitter_confirm']['subject'], message=message_body,
                    from_email=settings.EMAIL_HOST_USER, recipient_list=[sin.user.email])
        logger.info('Mail Sent!')
        return True
    except:
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.error("Error Occurred Sending Mail: %s, \n :%s \n :%s \n", e, f, g)
        return False

    # TODO: replace second argument with new field on SIN: approver [user]
def approve_submitter(sin, approver):
    logger = DebugLogger("sinwebapp.api.email_manager.approve_submitter").get_logger()

    logger.info('Confirming SIN # %s Submission Status %s For: %s To Approver: %s', 
                    sin.sin_number, sin.status.name, sin.user.email, approver.email )

    message_body = get_template()['submitter_approve']['body']
    message_body = message_body.format(CHANGE_REQUEST_TYPE=sin.status.name, SIN=sin.sin_number, 
                                        DATE=datetime.now(), APPROVAL_DATE=datetime.now(),
                                        APPROVAL_EMAIL=approver.email, SUBMITTED_NAME=sin.user.username,
                                        SUBMITTER_EMAIL=sin.user.email)
    logger.info('Email Body: %s', message_body)
    try:
        send_mail(subject=get_template()['submitter_approve']['subject'], message=message_body,
                    from_email=settings.EMAIL_HOST_USER, recipient_list=[sin.user.email])
        logger.info('Mail Sent!')
        return True
    except:
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.error("Error Occurred Sending Mail: %s, \n :%s \n :%s \n", e, f, g)
        return False

def deny_submitter(sin, reviewer):
    pass

def terminate_submitter(sin, approver):
    pass

def terminate_approver(sin, approver):
    pass

    # TODO: replace second argument with new field on SIN: reviewer [user]
def notify_reviewer(sin, reviewer):
    logger = DebugLogger("sinwebapp.api.email_manager.notify_reviewer").get_logger()

    logger.info('Confirming SIN # %s Submission Status %s For: %s To Reviewer: %s', 
                    sin.sin_number, sin.status.name, sin.user.email, reviewer.email )

    message_body = get_template()['reviewer_notify']['body']
    message_body = message_body.format(CHANGE_REQUEST_TYPE=sin.status.name, SIN=sin.sin_number, DATE=datetime.now(),
                                        REVIEWER_EMAIL=reviewer.email, SUBMITTED_NAME=sin.user.username,
                                        SUBMITTER_EMAIL=sin.user.email, LINK_TO_APP=settings.PRODUCTION_URL)
    logger.info('Email Body: %s', message_body)
    
    try:
        send_mail(subject=get_template()['reviewer_notify']['subject'], message=message_body,
                    from_email=settings.EMAIL_HOST_USER, recipient_list=[reviewer.email])
        logger.info("Mail Sent!")
        return True
    except:
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.error("Error Occurred Sending Mail: %s, \n :%s \n :%s \n", e, f, g)
        return False

    # TODO: replace second argument with new field on SIN: approver [user]
def notify_approver(sin, approver):
    logger = DebugLogger("sinwebapp.api.email_manager.notify_approver").get_logger()

    logger.info('Confirming SIN # %s Submission Status %s For: %s To Approver: %s', 
                    sin.sin_number, sin.status.name, sin.user.email, approver.email )

    message_body = get_template()['approver_notify']['body']
    message_body = message_body.format(CHANGE_REQUEST_TYPE=sin.status.name, SIN=sin.sin_number, DATE=datetime.now(),
                                        SUBMITTED_NAME=sin.user.username, SUBMITTER_EMAIL=sin.user.email, 
                                                    LINK_TO_APP=settings.PRODUCTION_URL)
    logger.info('Email Body: %s', message_body)
    
    try:
        send_mail(subject=get_template()['approver_notify']['subject'], message=message_body,
                    from_email=settings.EMAIL_HOST_USER, recipient_list=[approver.email])
        logger.info("Mail Sent!")
        return True
    except:
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.error("Error Occurred Sending Mail: %s, \n :%s \n :%s \n", e, f, g)
        return False