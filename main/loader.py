from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import os
# import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main.utils.middleware import CheckBotActivity, ThrottleMiddleware

from main.utils import s3_data_sync
from pathlib import Path
from main.config import PROJECT_NAME, DB_PATH, ADMIN_TG_ID
from main.utils.bot_activity_set import bot_activity_set

from main.utils.history_utils import add_to_history as h

# from main.handlers import router as router
# from main.routers.test_router import router as test_router
# from main.routers.last_router import router as last_router

# todo прописать планировщик отдельно и подключать роутеры тут, в лодыре
# from main.handlers import router as router
# from main.routers.test_router import router as test_router
# from main.routers.last_router import router as last_router

h('........запущен loader........')

load_dotenv()
BOT_NAME = os.getenv('BOT_NAME')
print(BOT_NAME)
bot = Bot(token=os.getenv('TOKEN'))
h('получен токен бота')

dp = Dispatcher()
# dp.include_routers(router, test_router, last_router)
h('роутеры подключены к диспетчеру')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
BOT_ACTIVITY_PATH = os.path.join(BASE_DIR, "config", "bot_activity.json")

# Включаем бота:
bot_activity_set(path=BOT_ACTIVITY_PATH, status=True)
dp["bot_enabled"] = True
h('признакам включения бота присвоено значение True')

# Подключаем middleware как outer_middleware:
dp.update.outer_middleware(CheckBotActivity(BOT_ACTIVITY_PATH))
dp.update.outer_middleware(ThrottleMiddleware(rate_limit=1))
h('подключили middleware')

# # Подключаем роутеры
# dp.include_routers(router, test_router, last_router)

# Подтягиваем логи сразу при включении бота
# todo переписать с использованием FILE_PATH = Path() / DIR_PATH / "history.txt"
s3_pref = str(Path(PROJECT_NAME, BOT_NAME, DB_PATH, 'logs')).replace("\\", "/")
local_dir = str(Path(DB_PATH, 'logs')).replace("\\", "/")
print(f'подтягиваем логи из {s3_pref} в {local_dir}')
s3_data_sync.all_s3_to_local(s3_prefix=s3_pref, local_dir=local_dir)
h('подтянули логи')

# Подключаем планировщик
scheduler = AsyncIOScheduler()  # подключение планировщика
scheduler_task_running = False  # переменная-флаг - делаем True, пока к.-л. задача выполняется
dp["task_is_running"] = False  # Флаг о выполнении к.-л. задачи в данный момент
h('подключен планировщик')

h('loader отработал')
