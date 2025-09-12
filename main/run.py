import logging
import asyncio
from main.handlers import router as router
import os
from main.utils.periodic_tasks import task_data_sync_s3
from main.utils.middleware import CheckBotActivity, ThrottleMiddleware
from main.loader import bot, dp, scheduler, logger
from main import bot_activity_set

# from main.utils.filters import FilterIsAdmin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

BOT_ACTIVITY_PATH = os.path.join(BASE_DIR, "config", "bot_activity.json")

dp.update.outer_middleware(CheckBotActivity(BOT_ACTIVITY_PATH))
dp.update.outer_middleware(ThrottleMiddleware(rate_limit=1))

print(f'распечатано из run.py, dp_bot_enabled = {dp.get("dp_bot_enabled", True)}')

logger.info("Бот стартует")


async def main():
    # Полдключаем роутеры:
    dp.include_router(router)

    # Запускаем планировщик:
    scheduler.add_job(task_data_sync_s3, "interval", seconds=3600, name='Сохранение данных в S3', id='data_dump_s3')
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
#
