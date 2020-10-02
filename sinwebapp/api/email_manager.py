from django.core.mail import send_mail
from core import settings
from datetime import datetime
from debug import DebugLogger
from os import sys

submitter_confirmation_subject="Core Contract Data Automation: Change Request Confirmation"
submitter_approval_subject="Core Contract Data Automation: Change Request Approved"
submitter_denied_subject="Core Contract Data Automation: Change Request Denied"
reviewer_notify_subject="Core Contract Data Automation: Change Request Received - Review Pending"
approver_notify_subject=""

submitter_confirmation_body="This email confirms that your {CHANGE_REQUEST_TYPE} was submitted for {SIN}.\n \n "+\
"Request made on: {DATE}\n SIN: {SIN}\n Submitter: {SUBMITTED_NAME}\n Submitter email: {SUBMITTER_EMAIL}\n "+\
"Reviewer: {REVIEWER_EMAIL}\n \n This email confirms a change has been submitted and is not confirmation "+\
"that your change has been successfully processed and approved. A notification will be sent once the change"+\
" request has been reviewed.\n \n If you have any questions regarding this request, please contact us."
submitter_approval_body="This email confirms that your {CHANGE_REQUEST_TYPE} was reviewed and approved for {SIN}. \n \n"+\
"Request made on: {DATE} \n Approval Date: {APPROVAL_DATE} \n SIN: {SIN} \n Submitter: {SUBMITTED_NAME} \n "+\
"Submitter email: {SUBMITTER_EMAIL} \n Reviewer: {APPROVAL_EMAIL} \n \n If you have any questions regarding "+\
"this request, please contact us."
submitter_denied_body=""
reviewer_confirmation_body="A {CHANGE_REQUEST_TYPE} was submitted for {SIN}. You are receiving this notification because"+\
"you were listed as the reviewer for the following {CHANGE_REQUEST_TYPE}. \n \n Please review the change request and"+\
"approve / deny the request through the Core Contract Data Automation Application. {LINK_TO_APP} \n \n If you have "+\
"any questions regarding this request or believe you received this notification in error, please contact us. \n \n \n "+\
" Submitter: {SUBMITTED_NAME} \n  Submitter email: {SUBMITTER_EMAIL} \n Request made on: {DATE} \n"
approver_notify_body=""

    # TODO: replace second argument with new field on SIN: reviewer [user]
def confirm_submitter(sin, reviewer):
    logger = DebugLogger("sinwebapp.api.email_manager.confirm_submitter").get_logger()

    logger.info('Confirming SIN # %s Submission Status %s For: %s To Reviewer: %s', 
                    sin.sin_number, sin.status.name, sin.user.email, reviewer.email )

    message_body=submitter_confirmation_body.format(CHANGE_REQUEST_TYPE=sin.status.name, SIN=sin.sin_number, DATE=datetime.now(),
                                                    REVIEWER_EMAIL=reviewer.email, SUBMITTED_NAME=sin.user.username,
                                                    SUBMITTER_EMAIL=sin.user.email)
    logger.info('Email Body: %s', message_body)

    try:
        send_mail(subject=submitter_confirmation_subject, message=message_body,
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

    message_body=submitter_approval_body.format(CHANGE_REQUEST_TYPE=sin.status.name, SIN=sin.sin_number, 
                                                    DATE=datetime.now(), APPROVAL_DATE=datetime.now(),
                                                    APPROVAL_EMAIL=approver.email, SUBMITTED_NAME=sin.user.username,
                                                    SUBMITTER_EMAIL=sin.user.email)
    logger.info('Email Body: %s', message_body)
    try:
        send_mail(subject=submitter_approval_subject, message=message_body,
                    from_email=settings.EMAIL_HOST_USER, recipient_list=[approver.email])
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

    # TODO: replace second argument with new field on SIN: reviewer [use
def notify_reviewer(sin, reviewer):
    logger = DebugLogger("sinwebapp.api.email_manager.notify_reviewer").get_logger()

    logger.info('Confirming SIN # %s Submission Status %s For: %s To Reviewer: %s', 
                    sin.sin_number, sin.status.name, sin.user.email, reviewer.email )
    message_body=reviewer_confirmation_body.format(CHANGE_REQUEST_TYPE=sin.status.name, SIN=sin.sin_number, DATE=datetime.now(),
                                                REVIEWER_EMAIL=reviewer.email, SUBMITTED_NAME=sin.user.username,
                                                SUBMITTER_EMAIL=sin.user.email, LINK_TO_APP=settings.PRODUCTION_URL)
    logger.info('Email Body: %s', message_body)
    
    try:
        send_mail(subject=reviewer_notify_subject, message=message_body,
                    from_email=settings.EMAIL_HOST_USER, recipient_list=[reviewer.email])
        logger.info("Mail Sent!")
        return True
    except:
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.error("Error Occurred Sending Mail: %s, \n :%s \n :%s \n", e, f, g)
        return False

def notify_approver(sin, approver):
    pass