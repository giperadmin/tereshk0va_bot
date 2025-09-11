import json
import os
import time

# from main.loader import dp

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
BOT_ACTIVITY_PATH = os.path.join(PARENT_DIR, "config", "bot_activity.json")


def bot_activity_get(path: str = BOT_ACTIVITY_PATH) -> bool:
    with open(f'{path}', 'r', encoding='utf-8') as file:
        bot_status = json.load(file)
    bot_activity = bot_status.get('bot_enabled', True)
    return bot_activity


# def set_bot_activity(path: str, status: bool):
#     bot_status: dict
#     with open(f'{path}', 'r', encoding='utf-8') as file:
#         bot_status = json.load(file)
#     bot_status.update({"bot_enabled": status})
#     with open(f'{path}', 'w', encoding='utf-8') as file:
#         # noinspection PyTypeChecker
#         json.dump(bot_status, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(BASE_DIR)
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.dirname(CURRENT_DIR)
    BOT_ACTIVITY_PATH = os.path.join(PARENT_DIR, "config", "bot_activity.json")
    print(BOT_ACTIVITY_PATH)

    s = True
    for n in range(99):
        s = not s
        set_bot_activity(path=BOT_ACTIVITY_PATH, status=s)
        print(f'{n} {bot_activity_get(BOT_ACTIVITY_PATH)}')
        time.sleep(5)
