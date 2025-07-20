"""
Утилита по сохранению данных в файле *.json
Исходные данные:
1. Словарь или список - data
2. Имя создаваемого файла json.
3. Путь к файлу.
4. Отметка о дописывании или перезаписывании данных:
    Если overwrite=True, то данные будут заменены новыми,
    а иначе - дописываться.
Возвращаем отчёт о результатах работы утилиты (return report)
"""

import json, time, random
from json import JSONDecodeError

from filelock import FileLock, Timeout


def save_as_json(data, filename: str = 'noname.json',
                 folderpath: str = '../main/datas/',
                 overwrite: bool = False
                 ):
    lock = FileLock(f'{folderpath}{filename}.lock')
    try:
        with lock.acquire(timeout=2):
            try:
                if not overwrite:
                    with open(f'{folderpath}{filename}', 'r', encoding='utf-8') as file:
                        database = json.load(file)
                    if type(data) != dict or type(database) != dict:
                        return "Пока можно дописывать только словари"
                    database.update(data)
                    with open(f'{folderpath}{filename}', 'w', encoding='utf-8') as file:
                        # noinspection PyTypeChecker
                        json.dump(database, file, ensure_ascii=False, indent=4)
                    return "Данные в базе обновлены (дописаны)"
                else:
                    with open(f'{folderpath}{filename}', 'w', encoding='utf-8') as file:
                        # noinspection PyTypeChecker
                        json.dump(data, file, ensure_ascii=False, indent=4)
                    return "Данные в базе заменены"
            except FileNotFoundError:
                with open(f'{folderpath}{filename}', 'w', encoding='utf-8') as file:
                    # noinspection PyTypeChecker
                    json.dump(data, file, ensure_ascii=False, indent=4)
                return 'Создан новый файл'
            except JSONDecodeError:
                return 'Ошибка декодирования'
            except:
                return 'Неизвестная ошибка 1'
    except:
        return 'Неизвестная ошибка 2'
