# modules
import smtplib
from email.message import EmailMessage

# content
sender = "onem2mserver@outlook.com"
reciever = input("Enter the reciever's email address: ")
password = input("Enter your password: ")
msg_body = 'Email sent using outlook!'
         

class Email:
    def __init__(self, sender, reciever, password):
        self.sender = sender
        self.reciever = reciever
        self.password = password
        self.msg_body = "Default email from Onem2m server"
    
    def send_email(self,msg_body):
        self.msg_body = msg_body
        msg = EmailMessage()
        msg['subject'] = 'Email sent using outlook.'   
        msg['from'] = self.sender
        msg['to'] = self.reciever
        msg.set_content(self.msg_body)
        
        print("Setting up a secure connection...")
        with smtplib.SMTP_SSL('smtp-mail.outlook.com', 465) as smtp:
            print("Logging in...")
            smtp.login(self.sender,self.password)
            print("Sending email...")
            smtp.send_message(msg)

new_email = Email(sender, reciever, password)

new_email.send_email(msg_body)