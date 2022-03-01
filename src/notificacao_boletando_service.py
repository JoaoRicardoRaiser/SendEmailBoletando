import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

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
        my_interest_publication_links = []
        my_interest_publications = []

        for publication in publications:
            publication_relevant_info = self.__get_relevant_informations(publication)

            publication_text = publication_relevant_info.text
            publication_link = publication_relevant_info.next['href']

            if self.__is_my_interest(publication_text) and publication_link not in self.__last_links:
                print(publication_text)
                print(publication_link)
                my_interest_publication_links.append(publication_link)
                my_interest_publications.append(publication)

        message = self.__create_message(my_interest_publication_links, my_interest_publications)

        if len(my_interest_publication_links) > 0:
            self.__email_sending_service.send_boletando_promotion(message)
            for publication in my_interest_publication_links: self.__last_links.append(publication)

        self.__check_update_controller_informations()

    @staticmethod
    def __create_message(publication_links: List[str], publications: List[Tag]) -> MIMEMultipart:
        text = ""
        for i in range(len(publication_links)):
            price = publications[i].find_next(class_="rh_regular_price").text

            name_and_link_div_info = publications[i].find_next(class_="flowhidden mb10 fontnormal position-relative")
            publication_link = name_and_link_div_info.a["href"]
            publication_name = name_and_link_div_info.text

            text += f"""
                    Modelo: {publication_name}
                    Link: {publication_link}
                    Preço: {price}
                    
                    
            """

        message = MIMEMultipart()
        message.attach(MIMEText(text, 'plain', "utf-8"))
        return message

    @staticmethod
    def __is_my_interest(publication_text: str) -> bool:
        if (
                publication_text.__contains__("3060") or
                publication_text.__contains__("2060") or
                publication_text.__contains__("3050") or
                publication_text.__contains__("3070") or
                publication_text.__contains__("1650") or
                publication_text.__contains__("Monitor")
        ):
            return True
        return False

    @staticmethod
    def __get_relevant_informations(publication: Tag):
        rel_info = publication.find_next(class_="flowhidden mb10 fontnormal position-relative")
        rel_info_on_fire = publication.find_next(class_="flowhidden mb10 fontnormal position-relative hoticonfireclass")
        return rel_info if rel_info is not None else rel_info_on_fire

    def __check_update_controller_informations(self) -> None:
        day_of_intance = self.__instance_time.day
        if day_of_intance == day_of_intance + 1:
            self.__instance_time = datetime.datetime.now()
            self.__last_links.clear()
