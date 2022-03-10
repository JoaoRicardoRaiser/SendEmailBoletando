import datetime
import os
import time

from src.notificacao_boletando_service import NotificationBoletandoService


def run():
    notificationService = NotificationBoletandoService()
    should_check_new_promotions = bool(os.getenv("SHOULD_CHECK_NEW_PROMOTIONS"))
    scheduler_time = int(os.getenv("SCHEDULER_TIME"))

    while should_check_new_promotions:
        print(f"Iniciando busca as: {datetime.datetime.utcnow().hour - 3}")
        notificationService.check_new_promotions()
        print(f"Finalizando busca as: {datetime.datetime.utcnow().hour - 3}")
        time.sleep(scheduler_time)


if __name__ == '__main__':
    run()
