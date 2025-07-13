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

import json
from json import JSONDecodeError

from filelock import FileLock, Timeout


async def save_as_json(data, filename: str = 'noname.json',
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


async def read_from_json(folderpath: str, filename: str) -> dict | list:
    lock = FileLock(f'{folderpath}{filename}.lock')
    try:
        with lock.acquire(timeout=2):
            try:
                with open(f'{folderpath}{filename}', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                if type(data) != dict:
                    print('')
                # print(str(data))
                return data
            except FileNotFoundError:
                print('FileNotFoundError в read_from_json')
                return {'ошибка': 'FileNotFoundError'}
            except JSONDecodeError:
                print('JSONDecodeError в read_from_json')
                return {'ошибка': 'JSONDecodeError в read_from_json'}
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                return {'ошибка': f"Произошла ошибка: {e}"}
            except:
                print('исключение в read_from_json')
                return {'ошибка': 'исключение в read_from_json'}
    except:
        print('')
        return {'ошибка': 'ПРЯМ СРАЗУ В read_from_json'}
    pass


if __name__ == "__main__":
    save_as_json(12345, '../../datas')
