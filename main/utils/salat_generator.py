from datas.ingredients import INGREDIENTS

import asyncio, random

TITLES = ['🥬Зелёное', '🥕Хрустящее', '🍋🍭Кислое/сладкое', '🌯Сытное', '☕Ароматное']


async def salat_generator(with_titles: bool = True) -> str:
    txt = ''
    i = 0
    for key in INGREDIENTS.keys():
        a = 0
        b1 = len(INGREDIENTS.get(key)) - 1
        r = random.randint(0, b1)
        # p = str(i + 1) + '. '
        s = ':\n'  # разделитель после заголовка ингредиентов
        s2 = '\n'  # разделитель после ингредиентов
        title = ''
        defis = '➖'
        if with_titles: title = (TITLES[i] + s)
        ingr = INGREDIENTS.get(key)[r] + s2
        txt = txt + defis + title + ingr
        i += 1
    composition = txt

    return composition
