import os
import smtplib
from email.mime.multipart import MIMEMultipart


class EmailSendingService:

    def __init__(self):
        self.__password = os.getenv("SENDER_EMAIL_PASSWORD")
        self.__sender_email = os.getenv("SENDER_EMAIL")
        self.__port = int(os.getenv("GMAIL_SMPT_PORT"))
        self.__smtp_server = os.getenv("GMAIL_SMTP_HOST")

    def send_boletando_promotion(self, message: MIMEMultipart) -> None:
        EmailSendingService.__add_reference_data(message)
        try:
            server = smtplib.SMTP(self.__smtp_server, self.__port)
            server.ehlo()
            server.starttls()
            server.login(self.__sender_email, self.__password)
            server.sendmail(message['From'], message['To'], message.as_string())
            server.close()

            print('successfully sent the mail')
        except Exception as e:
            print(f"Error: {e}")
            return e

    @staticmethod
    def __add_reference_data(message: MIMEMultipart) -> None:
        sender_email = os.getenv("SENDER_EMAIL")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        subject = os.getenv("SUBJECT_EMAIL")

        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

    @staticmethod
    def connection_is_open(connection):
        try:
            status = connection.noop()[0]
        except:
            status = -1
        return True if status == 250 else False
