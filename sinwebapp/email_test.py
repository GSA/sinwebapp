import smtplib
gmail_user = "sinweb@cloud.gov" 
#gmail_password = 
receiver = ['grant.moore@gsa.gov']

message = "tests"

try:
    server = smtplib.SMTP("smtp.gsa.gov")
    server.sendmail(gmail_user, receiver, message)
    #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    #server.ehlo()
    #server.login(gmail_user, gmail_password)
    #server.sendmail(gmail_user, receiver, message)
    #server.close()
    print("send")
except SMTPException:
    print("unable to send")
