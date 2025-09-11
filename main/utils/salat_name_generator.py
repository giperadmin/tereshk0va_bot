import json, random, re
import main.utils.work_with_json as work_with_json
from aiogram.fsm.context import FSMContext
from main import DB_PATH


async def salat_name_constructor(words: dict = None, composition: str = None) -> dict:
    """конструируем фразу из набранных слов"""
    singular = await singular_generator(composition)
    txt = (words.get("adjective") +
           " салат \"" + words.get("salats").capitalize() + "\"" + singular +
           " от жителей созвездия " + words.get("constellation").capitalize())
    emodzi = words.get("emodzi")
    words.clear()
    words["about"] = txt
    words["emodzi"] = emodzi
    return words


async def salat_name_generator(composition: str, state: FSMContext = None) -> dict:
    """генерация эпитета для салата, названия салата и созвездия на основе списков из файлов .json"""

    DATA_SOURCE = {
        "adjective": "list_adjective.json",  # эпитеты
        "salats": "list_salats.json",  # варианты названий салатов
        "constellation": "list_stars_constellation.json",  # созвездия
        "emodzi": "emodzi.json"  # эмодзи они же смайлики
    }
    data = await state.get_data()  # получаем данные из FSM
    # Названия полей в data (FSM) совпадают с ключами словаря -=DATA_SOURCE=-

    # проверяем, все ли поля есть в data и если какого-то поля нет, загружаем в него слова из .json
    for field in DATA_SOURCE.keys():
        if field not in data:
            fn = DATA_SOURCE[field]
            words = await work_with_json.read_from_json(folderpath=DB_PATH, filename=fn)
            # print (words) # todo
            random.shuffle(words)  # - перемешиваем список
            data[field] = words  # записываем список в FSM

    # выхватываем по одной произвольной записи из этих списков и записываем в итоговый словарь
    words = {}
    for field in DATA_SOURCE.keys():
        random.shuffle(data[field])  # - перемешиваем список ещё разок (это может отвлекать ресурсы)
        words[field] = data[field].pop()

    # если закончились слова в каком-то списке в data, то подгружаем туда новый список
    for field in DATA_SOURCE.keys():
        # print('field:',field,' --> len(data[field]):',len(data[field]))
        if not data[field]:
            fn = DATA_SOURCE[field]
            spisok = await work_with_json.read_from_json(folderpath=DB_PATH, filename=fn)
            random.shuffle(spisok)  # - перемешиваем список
            data[field] = spisok  # записываем список в data FSM
            print(f'Обновлено поле {field}')

    words = await salat_name_constructor(words, composition)  # конструируем из слов фразу
    await state.update_data(data)  # обновляем state FSM перед выходом
    return words  # возвращаем набранное как словарь


# todo добавить сюда список смайликов и может быть сразу два отзыва на хорошее и на плохое...


async def salat_name_generator_old(composition: str = "лук чеснок") -> str:
    salat_name_words = []
    file_names = ['words_adjective.json',
                  'words_salats.json',
                  'words_letter.json',
                  'words_stars_constellation.json'
                  ]
    adjective, salats, letter, constellation = [], [], [], []
    words_group = [adjective, salats, letter, constellation]


    for i in range(4):
        with open(f'{DB_PATH}{file_names[i]}', 'r', encoding='utf-8') as file:
            words_group[i] = list(json.load(file))

    for i in range(4):
        random_index = random.randint(0, len(words_group[i]) - 1)
        word = words_group[i][random_index]
        # print(word)
        salat_name_words.append(word)
    # print(salat_name_words)
    salat_name = (salat_name_words[0].lower() +
                  ' салат "' +
                  salat_name_words[1].capitalize() +
                  '"' +
                  await singular_generator(composition) +
                  ' от жителей ' +
                  # salat_name_words[2] +
                  ' созвездия ' +
                  salat_name_words[3].capitalize()
                  )
    return salat_name


async def singular_generator(composition: str) -> str:  # выявление особенных ингредиентов из состава салата
    # composition - это рецепт
    # Удаляем из текста рецепта всё, кроме букв и цифр:
    words = [re.sub(r'\W', '', word).lower() for word in composition.split()]  # это строка deepseek
    # получаем словарь с особенностями в дательном падеже
    fn = 'words_singularity.json'
    singular_dict = {}
    singular_dict = await work_with_json.read_from_json(folderpath=DB_PATH, filename=fn)
    singular = set()  # создаём пустое множество особенностей
    # выхватываем случайные ингредиенты из рецепта,
    # и если им сопоставлены особенности, добавляем во множество особенностей:
    while words:
        random.shuffle(words)
        word = words.pop()
        if word in singular_dict.keys():
            singular.add(singular_dict.get(word))
        if len(singular) > 1: break
    if len(singular) > 1:
        singular = ' с ' + singular.pop() + ' и ' + singular.pop()  # формируем фразу об особенностях салата
        return singular
    else:
        return ""


async def smile_generator() -> str:
    fp = DB_PATH
    fn = 'emodzi.json'
    smiles: list = await work_with_json.read_from_json(filename=fn, folderpath=fp)
    smile = smiles[random.randint(0, len(smiles) - 1)]
    return smile
