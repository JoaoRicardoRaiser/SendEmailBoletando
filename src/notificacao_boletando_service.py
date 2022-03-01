import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import Tag

from src.email_sending_service import EmailSendingService
from src.html_parser_service import HtmlParserService


class NotificationBoletandoService:

    def __init__(self) -> None:
        self.__last_links = []
        self.__instance_time = datetime.datetime.now()
        self.__email_sending_service = EmailSendingService()

    def check_new_promotions(self) -> None:
        publications = HtmlParserService.get_publications_boletando()
        for publication in publications:
            publication_relevant_info = publication.find_next(class_="flowhidden mb10 fontnormal position-relative")

            publication_text = publication_relevant_info.text
            publication_link = publication_relevant_info.next['href']

            if self.__is_my_interest(publication_text) and publication_link not in self.__last_links:
                print(publication_text)
                print(publication_link)

                message = self.__create_message(publication_link, publication)

                self.__email_sending_service.send_boletando_promotion(message)

                self.__last_links.append(publication_link)

        self.__check_update_controller_informations()

    @staticmethod
    def __create_message(publication_link: str, publication: Tag) -> MIMEMultipart:
        price = publication.find_next(class_="rh_regular_price").text
        message = MIMEMultipart()
        text = f"""
                Link: {publication_link}
                Preço: {price}
        """
        message.attach(MIMEText(text, 'plain', "utf-8"))
        return message

    @staticmethod
    def __is_my_interest(publication_text: str) -> bool:
        if (
                publication_text.__contains__("3060") or
                publication_text.__contains__("2060") or
                publication_text.__contains__("3050") or
                publication_text.__contains__("3070") or
                publication_text.__contains__("1650")
        ):
            return True
        return False

    def __check_update_controller_informations(self) -> None:
        day_of_intance = self.__instance_time.day
        if day_of_intance == day_of_intance + 1:
            self.__instance_time = datetime.datetime.now()
            self.__last_links.clear()
