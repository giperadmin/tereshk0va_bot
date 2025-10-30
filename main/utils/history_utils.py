from main.utils import time_utils
from pathlib import Path
from main.config import DB_PATH

DIR_PATH = Path() / DB_PATH
FILE_PATH = Path() / DIR_PATH / "history.txt"

MAX_LINES = 100000  # максимум строк в файле


def add_to_history(text: str = 'None',
                   folderpath: str = DIR_PATH,
                   filename: str = 'history.txt',  # todo добавить report
                   print_report: bool = False
                   ):
    """
    Добавляет строку в текстовый файл истории.
    Если файла нет — создаёт новый.
    Если строк больше MAX_LINES — оставляет только последние.
    """
    if not filename.endswith(".txt"): filename += '.txt'
    filepath = Path() / folderpath / filename
    # print(f"filepath = {filepath}")
    # filepath = filepath.relative_to("main")
    # print(f"преобразованный filepath = {filepath}")
    filepath.parent.mkdir(parents=True, exist_ok=True)  # создаём папки, если их нет
    
    time_msk = time_utils.get_time_msk()
    line = f"[{time_msk}] {text}\n"
    
    # создаст файл, если его нет
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(line)
    pass
    # проверяем количество строк
    with open(filepath, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        if len(lines) > MAX_LINES:
            f.seek(0)
            f.writelines(lines[-MAX_LINES:])
            f.truncate()
    if print_report: print(line)


if __name__ == '__main__':
    n: int
    print(f"DIR_PATH = {DIR_PATH}")
    print(f"FILE_PATH = {FILE_PATH}")
    for n in range(100):
        add_to_history('проверка')
        n += 1
