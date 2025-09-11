"""
Формирует дерево файлов и каталогов в формате строки.
"""
import os
import time
from pathlib import Path
from main.config.settings import DB_PATH

PATH_TO_ROOT = "../../"


def format_interval(seconds: int) -> str:
    days, seconds = divmod(seconds, 86400)  # 86400 секунд в дне
    hours, seconds = divmod(seconds, 3600)  # 3600 секунд в часе
    minutes, seconds = divmod(seconds, 60)  # 60 секунд в минуте
    """
    Пояснение:
    Функция divmod(a, b) возвращает кортеж: (divmod(a, b)) → (частное, остаток)
    То есть это как сразу сделать: a // b, a % b
    days, seconds = divmod(seconds, 86400):
    В days попадает количество полных дней, а в seconds остаётся остаток (то, что не уместилось в дни).
    Потом оставшиеся секунды переводятся в часы и минуты и т.д.
    """
    # И потом собираем:
    parts = []
    if days: parts.append(f"{days} дн")
    if hours: parts.append(f"{hours} ч")
    if minutes: parts.append(f"{minutes} мин")
    if seconds or not parts: parts.append(f"{seconds} сек")

    return " ".join(parts)


def format_tree(root_path: str = '.', indent="", last=True, time_limit: int = 3600) -> str:
    """
    Формирует дерево файлов и каталогов в формате строки.

    root_path: путь к корневой папке проекта
    indent: текущий отступ для дерева
    last: флаг, является ли текущий элемент последним в списке
    time_limit: время в секундах для определения "измененного файла"
    """

    tree_str = ""
    is_new_mark = " ──✨"
    basename = os.path.basename(root_path)

    # Определяем символ ветки
    branch = "└── " if last else "├── "
    tree_str += f"{indent}{branch}{basename}"

    # Если это файл, проверяем время изменения
    if os.path.isfile(root_path):
        mtime = os.path.getmtime(root_path)
        if time.time() - mtime <= time_limit:
            tree_str = tree_str + is_new_mark
        tree_str += "\n"
        return tree_str

    # Это папка
    tree_str += "/\n"
    indent += "    " if last else "│   "

    try:
        entries = sorted(os.listdir(root_path))
    except PermissionError:
        return tree_str + indent + "⛔\n"

    for i, entry in enumerate(entries):
        full_path = os.path.join(root_path, entry)
        tree_str += format_tree(full_path, indent, last=(i == len(entries) - 1), time_limit=time_limit)

    return tree_str


def get_directory_tree(path: str = '.', is_new: int = 60 * 5) -> str:
    # Если путь корректный, то получаем дерево каталогов:
    folder = Path(path)
    if folder.is_dir():
        relative_path = Path(path)
        absolute_path = relative_path.resolve()
        tree = format_tree(path, time_limit=is_new)
        tree = (f'\nОтносительный путь: {path}\n' +
                f'Абсолютный путь:\n{absolute_path}\n' +
                tree +
                f'символом ✨ отмечены файлы, сохранённые не ранее {format_interval(is_new)}\n')
        return tree
    else:
        return f'каталог {path} не найден'

# if __name__ == "__main__":
#     reading_path = "."  # Папка, из которой получаем дерево каталогов
#
#     dir_tree = get_directory_tree(path=reading_path, is_new=1 * 60 * 60 + 60*5)
#     print(dir_tree)
#
#     prefix_path = PATH_TO_ROOT + DB_PATH
#     project_path_2 = prefix_path  # Текущая папка проекта
#     dir_tree = get_directory_tree(path=project_path_2, is_new=316161651)
#     print(dir_tree)
