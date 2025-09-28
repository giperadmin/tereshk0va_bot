from dotenv import load_dotenv
import os

# Назначаемые параметры:
RATE_LIMIT=0.5 # задержка для антифлуда (время между сообщениями боту в миллисекундах)
SCHEDULER_INTERVAL = 9 # минуты интервал для дампа данных (в хранилище S3, например)
DB_PATH = "main/data/" # база данных на файлах .json, которая хранится внутри контейнера, локально
S3_DB_PATH = "tereshk0va_bot/storage/database/" # сюда будем делать дамп данных через каждые SCHEDULER_INTERVAL
PROJECT_NAME="tereshk0va_bot"


# Получаемые параметры:
load_dotenv()
ADMIN_TG_ID = int(os.getenv('ADMIN_TG_ID'))
# print(f"ADMIN_TG_ID = {ADMIN_TG_ID}")

