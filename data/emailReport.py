from datetime import datetime
import trade.tradeMechanics as tradeMechanics
import smtplib, ssl 
import other.creds as creds


def emailReport(ethReport, linkReport, btcReport, timeInterval):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = creds.emailSenderUsername  # Enter your address
    receiver_email = creds.emailRecieverUsername # Enter receiver address
    password = creds.emailSenderPassword
    message = 'Morning Report:\n Time Interval: {} \n ETH: {} \n BTC: {} \n LINK: {}'.format(timeInterval, ethReport, linkReport,btcReport)
    message = 'Subject: {}\n\n{}'.format('Talos Morning Report:{}'.format(datetime.date), message)


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

