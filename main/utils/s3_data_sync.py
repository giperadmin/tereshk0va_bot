import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from main.config.settings import DB_PATH
import hashlib
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import json
from pathlib import Path  # более современная, чем os
import mimetypes

# Получаем настройки:
load_dotenv()
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
REGION_NAME = "ru-1"

PATH_TO_ROOT = "../../" + DB_PATH  # todo это надо обдумать. Сделать универсальнее

# Создаём s3 клиент:
s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name=REGION_NAME
)


# Получение списка файлов по заданному пути:
def list_local(path_to_dir: str):
    """
    Возвращает список каталогов и файлов по указанному локальному пути
    """
    dirs = []
    files = []

    folder = Path(path_to_dir)
    if not folder.is_dir(): return print(f'каталог {path_to_dir} не найден')

    # Преобразование относительного пути в абсолютный
    relative_path = Path(path_to_dir)
    absolute_path = relative_path.resolve()
    print(absolute_path)

    with os.scandir(path_to_dir) as it:
        for entry in it:
            if entry.is_dir():
                dirs.append(entry.name)
            elif entry.is_file():
                files.append(entry.name)
    return dirs, files


# 1. Операции с каталогами:

def calculate_md5(file_path):
    """    Вычисляем MD5-хеш файла    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)  # type: ignore[arg-type]
    return hash_md5.hexdigest()


def sync_s3_to_local(s3_prefix: str = "", local_dir: str = DB_PATH):
    """
    Синхронизация с S3 на локальный диск
    :param s3_prefix: — это виртуальная "папка" или путь внутри S3-бакета. s3_prefix — это мощный инструмент для организации данных в S3, который работает как виртуальная файловая система, давая все преимущества структурированного хранения без реальных папок.
    :param local_dir: путь к каталогу (ld = '../' + DB_PATH)
    """
    s3_prefix.replace('\\', '/')
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=s3_prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            local_path = os.path.join(local_dir, key)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            action = "☁️➡️ ✅ Загружен новый"
            if os.path.exists(local_path):
                local_size = os.path.getsize(local_path)
                local_md5 = calculate_md5(local_path)
                s3_etag = obj["ETag"].strip('"')
                if local_size == obj["Size"] and local_md5 == s3_etag:
                    action = "☁️➡️ ⏩ Пропущен"
                else:
                    action = "☁️➡️ 🔄 Обновлён"

            if action != "☁️➡️ ⏩ Пропущен":
                s3.download_file(S3_BUCKET, key, local_path)

            print(f"{action}: {local_path}")


def sync_local_to_s3(local_dir: str = DB_PATH, s3_prefix: str = ""):
    """
    Загружает файлы из локального каталога в S3, если они отличаются (или если в бакете их нет).
    :param local_dir: путь к каталогу (ld = '../' + DB_PATH)
    :param s3_prefix: это виртуальная "папка" или путь внутри S3-бакета. s3_prefix — это мощный инструмент для организации данных в S3, который работает как виртуальная файловая система, давая все преимущества структурированного хранения без реальных папок.
    :return:
    """
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path: str = str(os.path.join(root, file)).replace("\\", "/")
            relative_path = os.path.relpath(local_path, local_dir).replace("\\", "/")
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")

            action = "-→☁️ ✅ Загружен новый"
            try:
                s3_head = s3.head_object(Bucket=S3_BUCKET, Key=s3_key)
                local_md5 = calculate_md5(local_path)
                s3_etag = s3_head["ETag"].strip('"')
                if os.path.getsize(local_path) == s3_head["ContentLength"] and local_md5 == s3_etag:
                    # action = "-→☁️  Пропущен"
                    action = None
                else:
                    action = "-→☁️ ✨ Обновлён"
            except ClientError as e:
                if e.response["Error"]["Code"] != "404":
                    raise

            if action != "→☁️ ⏩ Пропущен":
                s3.upload_file(local_path, Bucket=S3_BUCKET, Key=s3_key)

            if action: print(f"{action}: {local_path}")


def all_local_to_s3(local_dir: str = DB_PATH, s3_prefix: str = ""):
    """
    Загружает ВСЁ и ВСЯ из local_dir в S3
    :param local_dir: путь к каталогу (ld = '../' + DB_PATH)
    :param s3_prefix: префикс, который мы добавляем к ключу при загрузке целого каталога. Он нужен, чтобы загружать папку в S3 не в корень, а в определённый «виртуальный подкаталог». s3_prefix — это виртуальная "папка" или путь внутри S3-бакета.
    :return:
    """
    s3_prefix.replace('\\', '/')
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file).replace('\\', '/')

            # относительный путь внутри каталога
            relative_path = os.path.relpath(local_path, local_dir).replace('\\', '/')
            s3_path = os.path.join(s3_prefix, relative_path).replace("\\", "/")

            try:
                print(f"Загружаю {local_path} → s3://{S3_BUCKET}/{s3_path}")
                s3.upload_file(local_path, S3_BUCKET, s3_path)
            except NoCredentialsError:
                print("❌ Не найдены AWS credentials. Настройте их с помощью `aws configure`.")


def all_s3_to_local(s3_prefix: str = "", local_dir: str = DB_PATH):
    """
    Скачивает все файлы из указанного s3_prefix в бакете хранилища S3 в локальный каталог,
    сохраняя структуру папок.
    :param s3_prefix: префикс (папка) внутри S3, "" если корень
    :param local_dir: локальная папка для сохранения файлов
    """

    # Пагинатор нужен для обработки большого количества файлов
    paginator = s3.get_paginator("list_objects_v2")

    try:
        # Проходим по страницам объектов в бакете

        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=s3_prefix):
            if "Contents" in page:
                for obj in page["Contents"]:
                    s3_key = obj["Key"]  # полный путь объекта в S3

                    # Вычисляем относительный путь относительно префикса S3
                    relative_path = os.path.relpath(s3_key, s3_prefix)

                    # Создаем локальный путь для сохранения файла
                    local_path = os.path.join(local_dir, relative_path)

                    # Создаем папки, если их ещё нет
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)

                    # Загружаем файл из S3
                    print(f"Скачиваю s3://{S3_BUCKET}/{s3_key} → {local_path}")
                    s3.download_file(S3_BUCKET, s3_key, local_path)
    except NoCredentialsError:
        print("❌ Не найдены AWS credentials.")


# 2. Операции с файлами:


def put_data_s3_json(data: str | list | dict = "нет данных", s3_key: str = "noname",
                     open_in_browser: bool = False, print_report: bool = False) -> None:
    """
    сохраняет data в файл .JSON в хранилище S3. По умолчанию - браузер будет скачивать, а не открывать и без отчёта.
    :param data: строка, список или словарь для сохранения
    :param s3_key: путь в бакете S3 (если None, будет "noname")
    :param open_in_browser: открывать или скачивать в браузере. На это ещё влияет очистка данных браузера.
    :param print_report: вывод отчёта
    :return:
    """

    if not s3_key.endswith(".json"): s3_key += ".json"

    # inline - открыть в браузере, attachment - скачать:
    cont_disp = "inline" if open_in_browser else "attachment"

    json_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
    s3.put_object(Bucket=S3_BUCKET,
                  Key=s3_key,
                  Body=json_bytes,
                  ContentType="application/json",
                  ContentDisposition=cont_disp,
                  # ACL="public-read"  # делаем доступным по ссылке
                  )
    report = f"data сохр. на S3 методом put_object (.json) → https://s3.twcstorage.ru/{S3_BUCKET}/{s3_key}"
    if print_report: print(report)


def put_data_s3_txt(data: str | list | dict = "нет данных", s3_key: str = "noname",
                    json_dump: bool = False,
                    open_in_browser: bool = False, print_report: bool = False) -> None:
    """
    сохраняет data в файл .TXT в хранилище S3.
    По умолчанию:
        1. списки и словари преобразуются в строку методом str()
        2. браузер будет скачивать, а не открывать и без отчёта.
    :param data: строка, список или словарь для сохранения
    :param s3_key: путь в бакете S3 (если None, будет "noname")
    :param json_dump: "красивое" форматирование списков и словарей, как у .json - файлов. Метод
    :param open_in_browser: открывать или скачивать в браузере. На это ещё влияет очистка данных браузера.
    :param print_report: вывод отчёта
    :return:
    """
    if not s3_key.endswith(".txt"): s3_key += ".txt"

    # Метод преобразования в строку:
    text_data = json.dumps(data, ensure_ascii=False, indent=4) if json_dump else str(data)

    # inline - открыть в браузере, attachment - скачать:
    cont_disp = "inline" if open_in_browser else "attachment"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=text_data.encode("utf-8"),  # строку нужно преобразовать в байты
        ContentType="text/plain; charset=utf-8",  # указываем кодировку для браузеров
        ContentDisposition=cont_disp,  # открывать в браузере
        # ACL="public-read"  # делаем доступным по ссылке
    )
    report = f"data сохр. на S3 методом put_object (.txt) → https://s3.twcstorage.ru/{S3_BUCKET}/{s3_key}"
    if print_report: print(report)


def file_to_s3(local_file_path: str, s3_key: str = None,
               open_in_browser: bool = False, print_report: bool = False):
    """
    Загружает локальный файл в S3. Можно загрузить так, чтобы открывалось в браузере, а не скачивалось.
    Для этого предусмотрено определение параметра "ContentType".
    :param local_file_path: путь к локальному файлу
    :param s3_key: путь в бакете S3 (если None, будет использовано имя файла)
    :param open_in_browser: открывать или скачивать в браузере. На это ещё влияет очистка данных браузера.
    :param print_report: вывод отчёта
    :return:
    """
    # todo добавить проверку и особую запись, если файл json

    # inline - открыть в браузере, attachment - скачать:
    cont_disp = "inline" if open_in_browser else "attachment"

    # для txt content_type особенный, остальное - автоматически:
    if local_file_path.endswith(".txt"):
        content_type = "text/plain; charset=utf-8"
    else:
        content_type, encoding = mimetypes.guess_type(local_file_path)

    # если путь не задан, используем только имя файла
    s3_key = s3_key or os.path.basename(local_file_path)

    try:
        s3.upload_file(local_file_path, S3_BUCKET, s3_key,
                       ExtraArgs={
                           "ContentType": content_type,  # правильный MIME-тип
                           "ContentDisposition": cont_disp
                           # "ACL": "public-read"  # делаем файл доступным по ссылке
                       })

        report = f"{local_file_path} \nзагружеен на S3 методом put_object (.txt) → https://s3.twcstorage.ru/{S3_BUCKET}/{s3_key}"
        if print_report: print(report)
    except Exception as e:
        print(f"❌ Ошибка при загрузке файла: {e}")


def file_from_s3_to_local(s3_key: str, local_path: str = None):
    """
    Скачивает файл из S3 в локальное хранилище.
    :param bucket: имя S3-бакета
    :param s3_key: ключ (путь) в бакете
    :param local_file_path: путь, куда сохранить файл локально
                            (если None — сохраняется с тем же именем, что и в S3)
    """
    try:
        if local_path is None:
            local_path = os.path.basename(s3_key)

        s3.download_file(S3_BUCKET, s3_key, local_path)
        print(f"Файл {local_path} скачан ✅.")
    except:
        print('что-то пошло не так')


if __name__ == "__main__":
    # sync_s3_to_local()
    # sync_local_to_s3()
    # all_local_to_s3()
    # all_s3_to_local()
    s3_key = ('752044words_salaс'
              'ts_old.json')
    lp = '../ИИИИИИ'
    file_from_s3_to_local(s3_key, local_path=lp)
