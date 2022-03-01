import datetime
import time

import requests
from flask import Flask

from src.notificacao_boletando_service import NotificationBoletandoService

app = Flask(__name__)


@app.route("/")
def index():
    notificationService = NotificationBoletandoService()

    for i in range(5):
        print(f"Iniciando busca as: {datetime.datetime.now()}")
        notificationService.check_new_promotions()
        print(f"Finalizando busca as: {datetime.datetime.now()}")
        time.sleep(1)

    requests.get("https://notificacao-boletando.herokuapp.com/")
    return "Realizada com sucesso."


if __name__ == '__main__':
    app.run()
