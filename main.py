import smtplib
import ssl
import time

import requests
from bs4 import BeautifulSoup

ultimos_liks = []


def start():
    while True:
        html = requests.get("https://boletando.com/").content
        soup = BeautifulSoup(html, 'html.parser')
        artigos = soup.find_all("h3", class_="flowhidden mb10 fontnormal position-relative")
        for artigo in artigos:
            textoDoArtigo = artigo.next.text
            linkDoArtigo = artigo.next['href']

            if ehDoMeuInteresse(textoDoArtigo) and linkDoArtigo not in ultimos_liks:
                print(textoDoArtigo)
                print(linkDoArtigo)
                ultimos_liks.append(linkDoArtigo)
                email(linkDoArtigo)

        time.sleep(60)


def ehDoMeuInteresse(textoDoArtigo: str) -> bool:
    if (
            textoDoArtigo.__contains__("3060") or
            textoDoArtigo.__contains__("2060") or
            textoDoArtigo.__contains__("3050") or
            textoDoArtigo.__contains__("3070")
    ):
        return True

    return False


def email(text: str):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "youremail@gmail.com"
    receiver_email = "youremail@gmail.com"
    password = "yourpassword"
    subject = "Promocao Boletando"

    message = f"""\
    Subject: {subject}
    From: {sender_email}

    {text}."""
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print("email enviado com sucesso")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == '__main__':
    start()
