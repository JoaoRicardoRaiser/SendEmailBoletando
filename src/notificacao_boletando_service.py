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

            has_corram_tag = self.__check_if_has_corram_tag(publication)

            if self.__is_my_interest(publication_relevant_info,
                                     has_corram_tag) and publication_link not in self.__last_links:
                print(publication_text)
                print(publication_link)
                my_interest_publication_links.append(publication_link)
                my_interest_publications.append(publication)

        message = self.__create_message(my_interest_publication_links, my_interest_publications)

        if len(my_interest_publication_links) > 0:
            try:
                self.__email_sending_service.send_boletando_promotion(message)
                for publication in my_interest_publication_links: self.__last_links.append(publication)
            except Exception as e:
                print(f"Ocorreu um erro ao enviar email: {e}")

        self.__check_update_controller_informations()

    @staticmethod
    def __create_message(publication_links: List[str], publications: List[Tag]) -> MIMEMultipart:
        text = ""
        for i in range(len(publication_links)):
            price = publications[i].find_next(class_="rh_regular_price").text

            name_and_link_div_info = publications[i].find_next(class_="flowhidden mb10 fontnormal position-relative")
            publication_link = name_and_link_div_info.next["href"]
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
    def __is_my_interest(publication_relevant_info: Tag, has_corram_tag: bool) -> bool:
        publication_text = publication_relevant_info.text
        if (
                publication_text.upper().__contains__("3060") or
                publication_text.upper().__contains__("2060") or
                publication_text.upper().__contains__("3050") or
                publication_text.upper().__contains__("3070") or
                publication_text.upper().__contains__("1650") or
                publication_text.upper().__contains__("MONITOR") or
                has_corram_tag
        ):
            return True
        return False

    @staticmethod
    def __get_relevant_informations(publication: Tag):
        info_publ = publication.find_next(class_="grid_desc_and_btn")
        rel_info = info_publ.find_next(class_="flowhidden mb10 fontnormal position-relative")
        rel_info_fire = info_publ.find_next(class_="flowhidden mb10 fontnormal position-relative hoticonfireclass")
        return rel_info if rel_info is not None else rel_info_fire

    @staticmethod
    def __check_if_has_corram_tag(publication: Tag):
        tag_corram = publication.find_next(class_="re-ribbon-badge left-badge badge_3")

        if not tag_corram.__eq__(None):
            return tag_corram.text.upper() == "CORRAM"

    def __check_update_controller_informations(self) -> None:
        day_of_intance = self.__instance_time.day
        if day_of_intance == day_of_intance + 1:
            self.__instance_time = datetime.datetime.now()
            self.__last_links.clear()
