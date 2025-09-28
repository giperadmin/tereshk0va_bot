import json
import os
import time
# from main.loader import dp
import random
# from main.loader import dp


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
BOT_ACTIVITY_PATH = os.path.join(PARENT_DIR, "config", "bot_activity.json")


def bot_activity_set(path: str = BOT_ACTIVITY_PATH, status: bool = True):
    bot_status: dict

    # print(f'запустилась bot_activity_set \nBOT_ACTIVITY_PATH = {BOT_ACTIVITY_PATH}, \nstatus = {status}')

    # Получаем текущий статус бота из файла json как словарь:
    with open(f'{path}', 'r', encoding='utf-8') as file:
        bot_status = json.load(file)
    # print(f'В json хранился словарь {bot_status}')

    # Обновляем параметр "bot_enabled" в словаре:
    bot_status.update({"bot_enabled": status})

    # Записываем обновлённый словарь в файл json:
    with open(f'{path}', 'w', encoding='utf-8') as file:
        # noinspection PyTypeChecker
        json.dump(bot_status, file, ensure_ascii=False, indent=4)



    with open(f'{path}', 'r', encoding='utf-8') as file:
        bot_status = json.load(file)
    print(f'bot_status: {bot_status}')
    
    # dp["dp_bot_enabled"] = status
    # print(f"dp[\"dp_bot_enabled\"] =  {dp["dp_bot_enabled"]}")

    # Получаем значение глобальной переменной:
    # bot_enabled = dp.get("bot_enabled", True)
    # print(f'текущее значение глобальной переменной {bot_enabled}')

    # Записываем требуемое состояние глобальной переменной:
    # dp["bot_enabled"] = status

    # print(f'в json записали:        {bot_status}, а в dp - {dp.get("bot_enabled", True)}')


if __name__ == '__main__':
    print(f'{dp.get("bot_enabled", True)}')

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(BASE_DIR)
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.dirname(CURRENT_DIR)
    BOT_ACTIVITY_PATH = os.path.join(PARENT_DIR, "config", "bot_activity.json")
    # print(BOT_ACTIVITY_PATH)
    bot_activity_set(path=BOT_ACTIVITY_PATH, status=True)

    for n in range(99):
        s = bool(random.randint(0, 1))
        print(f'\n\nслучайно выбранный статус          {s}')
        bot_activity_set(path=BOT_ACTIVITY_PATH, status=s)
        time.sleep(5)
