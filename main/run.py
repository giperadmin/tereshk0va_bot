import logging
import asyncio
from aiogram import Bot, Dispatcher  # F - класс чтобы пользоваться
from handlers import router as router

from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)  # опрашиваем телеграм на наличие новых событий в бесконечном цикле


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
