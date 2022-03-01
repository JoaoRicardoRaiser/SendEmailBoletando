import os
import smtplib
from email.mime.multipart import MIMEMultipart


class EmailSendingService:

    def __init__(self):
        __password = os.getenv("SENDER_EMAIL_PASSWORD")
        __sender_email = os.getenv("SENDER_EMAIL")

        self.__port = int(os.getenv("GMAIL_SMPT_PORT"))
        self.__smtp_server = os.getenv("GMAIL_SMTP_HOST")

        self.server = smtplib.SMTP(self.__smtp_server, self.__port)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(__sender_email, __password)

    def send_boletando_promotion(self, message: MIMEMultipart) -> None:
        EmailSendingService.__add_reference_data(message)
        try:
            self.server.sendmail(message['From'], message['To'], message.as_string())
            print('successfully sent the mail')
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def __add_reference_data(message: MIMEMultipart) -> None:
        sender_email = os.getenv("SENDER_EMAIL")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        subject = os.getenv("SUBJECT_EMAIL")

        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
