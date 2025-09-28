import logging, asyncio, os
from main.utils.periodic_tasks import task_data_sync_s3, task_copy_all_s3_to_cold_s3
from main.loader import bot, dp, scheduler

from main.handlers import router as router
from main.routers.test_router import router as test_router
from main.routers.last_router import router as last_router
from main import add_to_history as h

dp.include_routers(router, test_router, last_router)
h('подключили роутеры к диспетчеру')


async def main():
    # Запускаем планировщик:
    scheduler.add_job(task_copy_all_s3_to_cold_s3, "cron", minute=58,
                      name='Сохранение данных в S3 cold', id='data_dump_s3_cold')
    scheduler.add_job(task_data_sync_s3, "interval", seconds=60,
                      name='Сохранение данных в S3', id='data_dump_s3')
    scheduler.start()
    h('запустили планировщик')
    
    # Опрашиваем телеграм на наличие новых событий в бесконечном цикле:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # logging.getLogger("aiogram.dispatcher").setLevel(logging.CRITICAL) # fix
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
