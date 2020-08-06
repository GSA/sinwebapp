import smtplib, sys
from debug import DebugLogger

logger = DebugLogger("email_test").get_logger()


send_user = "grant.moore@gsa.gov" 
#send_user_password = 
receive_user = ['grant.moore@gsa.gov', 'chinchalinchin@gmail.com']
message = "testing testing 123"

logger.info("Testing email from %s to %s", send_user, receive_user)
try:
    logger.info("Opening SMTP connection to smtp.gsa.gov")
    server = smtplib.SMTP(host='smtp.gsa.gov', port=25, timeout=30)
    server.ehlo()
        #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #server.login(send_user, send_user_password)
    logger.info("Sending mail")
    server.sendmail(send_user, receive_user, message)
    logger.info("Closing SMTP connection to smtp.gsa.gov")
    server.close()

except:
    logger.warning("Unable To Send Email")
    e1 = sys.exc_info()[0]
    e2 = sys.exc_info()[1]
    e3 = sys.exc_info()[2]
    logger.warning("Error Type: %s", e1)
    logger.warning("Error Value: %s", e2)
    logger.warning("Error Stack: %s", e3)
