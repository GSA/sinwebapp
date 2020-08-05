import smtplib
from debug import DebugLogger

logger = DebugLogger("email_test").getlogger()


gmail_user = "sinweb@cloud.gov" 
#gmail_password = 
receiver = ['grant.moore@gsa.gov']
message = "testing testing 123"

logger.info("Testing email from %s to %s", gmail_user, receiver)
try:
    logger.info("Opening SMTP connection to smtp.gsa.gov")
    server = smtplib.SMTP("smtp.gsa.gov")
        #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #server.ehlo()
        #server.login(gmail_user, gmail_password)
    logger.info("Sending mail")
    server.sendmail(gmail_user, receiver, message)
    logger.info("Closing SMTP connection to smtp.gsa.gov")
    server.close()

except:
    e = sys.exc_info()[0]
    logger.warn("Unable To Send Email, Error: %s", e)
