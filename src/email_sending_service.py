import os
import smtplib
from email.mime.multipart import MIMEMultipart


class EmailSendingService:

    def __init__(self):
        port = int(os.getenv("GMAIL_SMPT_PORT"))
        smtp_server = os.getenv("GMAIL_SMTP_HOST")
        password = os.getenv("SENDER_EMAIL_PASSWORD")
        sender_email = os.getenv("SENDER_EMAIL")

        self.server = smtplib.SMTP(smtp_server, port)
        self.server.starttls()
        self.server.ehlo()
        self.server.login(sender_email, password)

    def send_boletando_promotion(self, message: MIMEMultipart) -> None:
        EmailSendingService.add_reference_data(message)

        try:
            self.server.sendmail(message['From'], message['To'], message.as_string())
            self.server.close()
            print('successfully sent the mail')
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def add_reference_data(message: MIMEMultipart) -> None:
        sender_email = os.getenv("SENDER_EMAIL")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        subject = os.getenv("SUBJECT_EMAIL")

        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
