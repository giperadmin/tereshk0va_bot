import time
from pickle import GLOBAL

from main.utils import s3_data_sync, directory_tree
from main.utils import s3_cold_data_sync
import os
from dotenv import load_dotenv
from main import DB_PATH, SCHEDULER_INTERVAL, PROJECT_NAME
from main import loader
from main.utils.history_utils import add_to_history as h

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
        h('ждём-с...')
        print(f'{tittle} ждём-с...')


def task_data_sync_s3():
    h('task_data_sync_s3 запущен')
    # Если какая-то задача с помощью переменной флага отметила свой запуск, то ждём её завершения:
    waiting()

    # С помощью переменной-флага отмечаем, что началось выполнение задачи:
    loader.scheduler_task_running = True

    # print(f'началось выполнение планировщика data_dump_s3 flag = {loader.scheduler_task_running}')
    # time.sleep(5)  # todo убрать эту задержку

    # Готовим пути:
    s3_pref = PROJECT_NAME + '/' + BOT_NAME + '/' + DB_PATH
    s3_pref.replace('\\', '/')

    print(f'Запускаем sync_local_to_s3 с s3_pref = {s3_pref}')

    # Запускаем синхронизацию:
    s3_data_sync.sync_local_to_s3(
        local_dir=DB_PATH,
        s3_prefix=s3_pref,

    )

    # Отключаем переменную-флаг:
    loader.scheduler_task_running = False
    # print(f'завершилось выполнение планировщика data_dump_s3 flag = {loader.scheduler_task_running}')
    h('task_data_sync_s3 отработал')

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

    print(f'\nЗапускаем all_local_to_s3 с DB_PATH = {DB_PATH}, s3_pref = {s3_pref}\n')

    # Запускаем синхронизацию:
    s3_data_sync.all_local_to_s3(local_dir=DB_PATH,s3_prefix=s3_pref)

    # Отключаем переменную-флаг:
    loader.scheduler_task_running = False
    # print(f'завершилось выполнение планировщика data_dump_s3 flag = {loader.scheduler_task_running}')
    h('task_data_dump_s3 отработал DUMP')

def task_sync_from_S3_to_local():
    h('task_sync_from_S3_to_local запущен')
    # Если какая-то задача с помощью переменной флага отметила свой запуск, то ждём её завершения:
    waiting()

    # С помощью переменной-флага отмечаем, что началось выполнение задачи:
    loader.scheduler_task_running = True

    # print(f'началось выполнение планировщика data_dump_s3 flag = {loader.scheduler_task_running}')
    time.sleep(5)  # todo убрать эту задержку

    # Готовим пути:
    s3_pref = PROJECT_NAME + '/' + BOT_NAME + '/' + DB_PATH
    s3_pref.replace('\\', '/')

    print(f'\nЗапускаем all_local_to_s3 с DB_PATH = {DB_PATH}, s3_pref = {s3_pref}\n')

    # Запускаем синхронизацию:
    s3_data_sync.sync_s3_to_local(s3_prefix=s3_pref,local_dir=DB_PATH)

    # Отключаем переменную-флаг:
    loader.scheduler_task_running = False
    # print(f'завершилось выполнение планировщика data_dump_s3 flag = {loader.scheduler_task_running}')
    h('task_sync_from_S3_to_local отработал')

def task_copy_all_s3_to_cold_s3():
    waiting()
    loader.scheduler_task_running = True
    s3_cold_data_sync.copy_all_s3_to_cold_s3()
    loader.scheduler_task_running = False
    h('task_copy_all_s3_to_cold_s3 отработал DUMP в COLD')