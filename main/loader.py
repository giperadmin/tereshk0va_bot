from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import os
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp["dp_bot_enabled"] = True
admin_tg_id = int(os.getenv('ADMIN_TG_ID'))

print(f'Печать из  loader.py: {admin_tg_id}')

scheduler = AsyncIOScheduler()  # подключение планировщика
scheduler_task_running = False  # переменная-флаг - делаем True, пока к.-л. задача выполняется

# Логирование:
logging.basicConfig(
    level=logging.INFO,  # Можно DEBUG, INFO, WARNING
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),  # вывод в консоль
        logging.FileHandler("main/data/logs/bot.log", encoding="utf-8")  # вывод в файл
    ])
logger = logging.getLogger(__name__)
"""
Теперь:
В любом месте проекта можешь писать:
from main.loader import logger

logger.info("Бот стартует")
logger.warning("Что-то пошло не так")
logger.error("Ошибка!")

Все сообщения попадут в консоль и в файл bot.log.
"""
