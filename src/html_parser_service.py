import os

import requests
from bs4 import BeautifulSoup


class HtmlParserService:

    @staticmethod
    def get_publications_boletando():
        link_boletando = os.getenv("LINK_BOLETANDO")
        html = requests.get(link_boletando).content
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find_all("div", class_="info_in_dealgrid")
