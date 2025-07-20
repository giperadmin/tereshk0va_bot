import json, random, re
from salat_generator import salat_generator
from utils import work_with_json_BETA as wwjb

fp = 'datas/'
fn = 'words_singularity.json'


def salat_name_generator(composition):
    def get_singular(composition):  # выявление особенных ингредиентов из состава салата
        # composition - это рецепт
        # Удаляем из текста рецепта всё, кроме букв и цифр:
        words = [re.sub(r'[^\w]', '', word).lower() for word in composition.split()]
        # получаем словарь с особенностями в дательном падеже
        singular_dict = wwjb.read_from_json(folderpath=fp, filename=fn)
        singular = set()  # создаём пустое множество особенностей
        # выхватываем случайные ингредиенты из рецепта,
        # и если им сопоставлены особенности, добавляем во множество особенностей:
        while len(singular) < 2:
            word = words[random.randint(0, len(words) - 1)]
            if word in singular_dict.keys():
                singular.add(singular_dict.get(word))
        print(singular)
        singular = ' с ' + singular.pop() + ' и ' + singular.pop()  # формируем фразу об особенностях салата
        return singular

    salat_name_words = []
    file_names = ['words_adjective.json',
                  'words_salats.json',
                  'words_letter.json',
                  'words_stars_constellation.json'
                  ]
    adjective, salats, letter, constellation = [], [], [], []
    words_group = [adjective, salats, letter, constellation]

    foldername = 'datas/'
    for i in range(4):
        with open(f'{foldername}{file_names[i]}', 'r', encoding='utf-8') as file:
            words_group[i] = list(json.load(file))

    for i in range(4):
        random_index = random.randint(0, len(words_group[i]) - 1)
        word = words_group[i][random_index]
        # print(word)
        salat_name_words.append(word)
    # print(salat_name_words)
    salat_name = (salat_name_words[0].lower() +
                  ' салат "' + salat_name_words[1].capitalize() + '"' +
                  get_singular(composition) +
                  ' от жителей ' +
                  salat_name_words[2].capitalize() +
                  ' созвездия ' +
                  salat_name_words[3].capitalize()
                  )
    return salat_name

composition=salat_generator(with_titles=False)
print(composition)
salat_name=salat_name_generator(composition= composition)
print(salat_name)
