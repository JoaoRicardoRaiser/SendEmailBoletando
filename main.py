import datetime
import os
import time

from src.notificacao_boletando_service import NotificationBoletandoService


def main():
    notificationService = NotificationBoletandoService()
    should_check_new_promotions = bool(os.getenv("SHOULD_CHECK_NEW_PROMOTIONS"))

    while should_check_new_promotions:
        print(f"Iniciando busca as: {datetime.datetime.now()}")
        notificationService.check_new_promotions()
        print(f"Finalizando busca as: {datetime.datetime.now()}")

        time.sleep(10)
        should_check_new_promotions = bool(os.getenv("SHOULD_CHECK_NEW_PROMOTIONS"))


if __name__ == '__main__':
    main()
