import smtplib
from email.message import EmailMessage

class smtpHandler:
    # initialize 
    def __init__(self, SERVER, USERNAME, PASSWORD, BCC_COPY):
        self.SERVER = SERVER
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.BCC_COPY = BCC_COPY
    
    # Send email
    def send(self, to, subject, body):
        smtpServ = smtplib.SMTP(self.SERVER, 587)
        smtpServ.ehlo()
        smtpServ.starttls()
        smtpServ.ehlo()
        smtpServ.login(self.USERNAME, self.PASSWORD)

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['FROM'] = self.USERNAME
        msg['TO'] = to
        msg['Bcc'] = self.BCC_COPY
        msg.set_content(body)
        smtpServ.send_message(msg)
        smtpServ.quit()