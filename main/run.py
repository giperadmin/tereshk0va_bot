import logging
import asyncio
from main.handlers import router as router
import os
from main.utils.periodic_tasks import task_data_sync_s3
from main.utils.middleware import CheckBotActivity, ThrottleMiddleware
from main.loader import bot, dp, scheduler
from main import bot_activity_set
from main.utils import s3_data_sync
from pathlib import Path
from main.config import PROJECT_NAME, DB_PATH
from main.loader import BOT_NAME

# from main.utils.filters import FilterIsAdmin

# Определяемся с путями:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
BOT_ACTIVITY_PATH = os.path.join(BASE_DIR, "config", "bot_activity.json")

# Подключаем middleware как outer_middleware:
dp.update.outer_middleware(CheckBotActivity(BOT_ACTIVITY_PATH))
dp.update.outer_middleware(ThrottleMiddleware(rate_limit=1))


# logger.info("Бот стартует")


async def main():
    # Полдключаем роутеры:
    dp.include_router(router)

    # Подтягиваем накопленные данные из хранилища S3
    # s3_data_sync.sync_s3_to_local()

    # Подтягиваем логи
    s3_pref = str(Path(PROJECT_NAME, BOT_NAME,DB_PATH,'logs')).replace("\\", "/")
    local_dir = str(Path(DB_PATH,'logs')).replace("\\", "/")
    print(f'подтягиваем логи из {s3_pref} в {local_dir}')
    s3_data_sync.all_s3_to_local(s3_prefix=s3_pref, local_dir=local_dir)


    # Запускаем планировщик:
    scheduler.add_job(task_data_sync_s3, "interval", seconds=60*5, name='Сохранение данных в S3', id='data_dump_s3')
    scheduler.start()

    # Опрашиваем телеграм на наличие новых событий в бесконечном цикле:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # logging.getLogger("aiogram.dispatcher").setLevel(logging.CRITICAL) # fix

    # Включаем бота:
    bot_activity_set(path=BOT_ACTIVITY_PATH, status=True)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')