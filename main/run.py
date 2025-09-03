import logging
import asyncio
from aiogram import Bot, Dispatcher  # F - класс чтобы пользоваться
from main.handlers import router as router
from datetime import datetime
from main.config.settings import SCHEDULER_INTERVAL
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))


# async def my_periodic_task():  # функция, которая будет выполняться с некоторой периодичностью
#         txt = "Прошло " + str(SCHEDULER_INTERVAL) + " сек."
#         now = datetime.now()
#         formatted = now.strftime("%d.%m.%Y %H:%M:%S,%f")[:-1]
#         txt = txt + '\n' + formatted
#         await bot.send_message(223852270, text=txt)
#
#
# async def scheduler():  # планировщик
#         while True:
#             await my_periodic_task()
#             await asyncio.sleep(SCHEDULER_INTERVAL)  # ждём 26 секунд


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    # asyncio.create_task(scheduler())  # эта команда запускает планировщик
    await dp.start_polling(bot)  # опрашиваем телеграм на наличие новых событий в бесконечном цикле


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # logging.getLogger("aiogram.dispatcher").setLevel(logging.CRITICAL) # fix
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
#