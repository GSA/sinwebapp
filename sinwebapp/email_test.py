import smtplib
from debug import DebugLogger

logger = DebugLogger("email_test").getlogger()


send_user = "sinweb@cloud.gov" 
#gmail_password = 
receive_user = ['grant.moore@gsa.gov']
message = "testing testing 123"

logger.info("Testing email from %s to %s", send_user, receive_user)
try:
    logger.info("Opening SMTP connection to smtp.gsa.gov")
    server = smtplib.SMTP("smtp.gsa.gov")
        #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #server.ehlo()
        #server.login(gmail_user, gmail_password)
    logger.info("Sending mail")
    server.sendmail(send_user, receive_user, message)
    logger.info("Closing SMTP connection to smtp.gsa.gov")
    server.close()

except:
    e = sys.exc_info()[0]
    logger.warn("Unable To Send Email, Error: %s", e)
