from aiogram import Bot, F, Router  # F - класс чтобы пользоваться фильтром
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from utils.salat_generator import salat_generator
import utils.salat_name_generator as sng
from utils.work_with_json import save_as_json, read_from_json
from aiogram.filters import CommandStart, Command
import keyboards as kb
import time
from datetime import datetime
from utils.answers import responses_to_bad_reviews as rtbr
from utils.middleware import ThrottleMiddleware  # Ограничение количества запросов от юзеров

router = Router(name='__name__')
router.message.middleware(ThrottleMiddleware(rate_limit=1.5))
router.callback_query.middleware(ThrottleMiddleware(rate_limit=1.5))


@router.message(CommandStart())
@router.message(F.text == 'Обнулить')
async def intro(message: Message, state: FSMContext):
    await state.clear()
    txt = 'Привет с орбиты! 🚀👽'
    await message.answer(text=txt, reply_markup=kb.main)


@router.message(F.text == 'Придумай салат!')  # F-фильтром можно ловить всё, что пришлют, текст, медиа...
async def test1(message: Message, bot: Bot, state: FSMContext):
    intro = 'Вот, какой изумительный рецепт я подобрала:\n👩🥘\n'
    composition = await salat_generator(with_titles=False)
    starline = '♡ ⋆｡˚ ✩° ｡⋆⛧⋆⁺ ｡˚⋆ ♡･ﾟ✧*・ﾟ✧ ♡⋆｡˚❁⋆｡°✩'
    p = '\n'
    salat_name = await sng.salat_name_generator(composition, state)
    txt = (intro + p + salat_name.get("about") + ':' + p + p
           + composition + p + salat_name["emodzi"] + p + starline + p)
    await message.answer(text=txt, reply_markup=kb.main3)

    data_key = str(time.time())
    data_item = (str(message.from_user.id) +
                 '; first_name: ' + str(message.from_user.first_name) +
                 '; last_name: ' + str(message.from_user.last_name) +
                 '; username: @' + str(message.from_user.username) +
                 '; is_premium: ' + str(message.from_user.is_premium))
    data = {data_key: data_item}
    current_date = datetime.now().strftime("%Y-%m-%d")
    await save_as_json(data,
                       filename=f'users_list_{current_date}.json',
                       folderpath='datas/logs/',
                       overwrite=False
                       )
    txt = str(message.from_user.first_name) + ' получил рецепт салата'
    await bot.send_message(223852270, text=txt)


@router.message(F.text == 'Подобрать заправку')
async def set_settings(message: Message):
    txt = 'Что вы хотите заправить?'
    await message.answer(text=txt, reply_markup=kb.main4)


@router.message(F.text.contains('Звездолёт'))
async def set_settings(message: Message):
    txt = ('Звездолёт 🛸 нужно заправлять редкими изотопами водорода и гелия. '
           'Ближайшая к вам заправка звездолётов откроется на Луне 🌔 (см. выше 🔭)).\n'
           'Дату открытия уточняйте.')
    await message.answer(text=txt, reply_markup=kb.main)


@router.message(F.text == 'Салат🥗')
async def set_settings(message: Message):
    txt = ('Ну неужели мне за вас решать, чем заправить салат?!\n'
           'Мужчинам - не жалейте майонеза, девочкам - чуточку оливкового масла (оно, оказывается, дорогое по калориям)')
    await message.answer(text=txt, reply_markup=kb.main2)


@router.message(F.text == 'Настройки')
async def set_settings(message: Message):
    txt = 'Настройки будут доступны в платной версии 😁 Шучу))) Просто положитесь на удачу)'
    await message.answer(text=txt, reply_markup=kb.main)


@router.message(F.text.contains("🔥") | F.text.contains("🚀"))
async def set_settings(message: Message):
    txt = 'Спасибо за отзыв 💋'
    await message.answer(text=txt, reply_markup=kb.main)


@router.message(F.text.contains("🤢"))
async def set_settings(message: Message, state: FSMContext):
    txt = await rtbr(state)
    await message.answer(text=txt, reply_markup=kb.main)


@router.message()
async def last_handler(message: Message):
    txt = '⚠️Ой, чот сломалося... Жмите кнопки внизу экрана!'
    await message.answer(text=txt, reply_markup=kb.main)
