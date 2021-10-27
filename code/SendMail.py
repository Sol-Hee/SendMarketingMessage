import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from customizing import MailText
import os
import boto3
import datetime

today = datetime.date.today()

driver = os.getenv('DRIVER')
host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER')
pwd = os.getenv('PWD')


# Create Session
def send():
    s = smtplib.SMTP(
        host=host,
        port=port,
    )

    s.starttls()
    s.login(user, pwd)

    msg = MIMEMultipart()
    msg['Subject'] = MailText.mail_subject
    msg.attach(MIMEText(MailText.mail_text))

    # File Read
    s3 = boto3.resource('s3')
    bucket = 'your_bucket'
    key = 'your_key/excel.xlsx'
    obj = s3.Object(bucket, key)
    attachment = obj.get()['Body'].read()

    part = MIMEApplication(attachment, Name=MailText.file_name)

    msg.attach(part)

    s.sendmail(
        MailText.from_addr,
        MailText.to_addr,
        msg.as_string()
    )

    s.quit()

    print('success!')
    return None