import json
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


folderpath = '../config/'
print(list_local(folderpath))
filename = 'bot activity.json'
data ={"bot_enabled":True}

with open(f'{folderpath}{filename}', 'w', encoding='utf-8') as file:
    # noinspection PyTypeChecker
    json.dump(data, file, ensure_ascii=False, indent=4)
