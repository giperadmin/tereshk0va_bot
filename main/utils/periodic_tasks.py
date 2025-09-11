import time
from pickle import GLOBAL

from main.utils import s3_data_sync, directory_tree
import os
from dotenv import load_dotenv
from main import DB_PATH, SCHEDULER_INTERVAL, PROJECT_NAME
from main import loader

BOT_NAME = os.getenv("BOT_NAME")


def waiting(tittle: str = '', period: int = 1):
    """
    Ждёт, пока переменная-флаг loader.scheduler_task_running не станет False,
    т.е. пока не завершится текущая задача
    :param tittle: - пояснеие, которое будет в принте
    :param period: - частота опроса переменной loader.scheduler_task_running, сек
    :return: None
    """
    while loader.scheduler_task_running:
        time.sleep(1)
        print(f'{tittle} ждём-с...')


def task_data_dump_s3():
    # Если какая-то задача с помощью переменной флага отметила свой запуск, то ждём её завершения:
    waiting()

    # С помощью переменной-флага отмечаем, что началось выполнение задачи:
    loader.scheduler_task_running = True

    # print(f'началось выполнение планировщика data_dump_s3 flag = {loader.scheduler_task_running}')
    time.sleep(5)  # todo убрать эту задержку

    # Готовим пути:
    s3_pref = PROJECT_NAME + '/' + BOT_NAME + '/' + DB_PATH
    s3_pref.replace('\\', '/')

    # Запускаем синхронизацию:
    s3_data_sync.sync_local_to_s3(
        local_dir=DB_PATH,
        s3_prefix=s3_pref)

    # Отключаем переменную-флаг:
    loader.scheduler_task_running = False
    # print(f'завершилось выполнение планировщика data_dump_s3 flag = {loader.scheduler_task_running}')
