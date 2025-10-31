from aiogram import Bot, F, Router  # F - класс чтобы пользоваться фильтром
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import or_f
from main.utils.salat_generator import salat_generator
import main.utils.salat_name_generator as sng
from main.utils.work_with_json import save_as_json, read_from_json
from aiogram.filters import CommandStart, Command
import main.keyboards as kb
import time
from datetime import datetime
from main.utils.answers import responses_to_bad_reviews as rtbr
from main.utils.middleware import ThrottleMiddleware  # Ограничение частоты запросов от юзеров
# from main import ThrottleMiddleware
from main import RATE_LIMIT, DB_PATH
from main.utils.bot_activity_set import bot_activity_set
from main.loader import dp
from main.utils.filters import FilterIsAdmin, FilterIsEnable
from main.utils.s3_data_sync import all_local_to_s3
from main.loader import scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import STATE_PAUSED, STATE_RUNNING
from main import loader, waiting, task_data_dump_s3, task_copy_all_s3_to_cold_s3
from main.routers import last_router
from main import add_to_history as h

router = Router(name='__name__')


# router.message.middleware(ThrottleMiddleware(rate_limit=RATE_LIMIT))
# router.callback_query.middleware(ThrottleMiddleware(rate_limit=RATE_LIMIT))


@router.message(CommandStart())
@router.message((F.text.lower() == 'обнулить') | (F.text.lower() == 'обнулись'))
# @router.message(or_f(CommandStart(), (F.text.in_(['Обнулить'])))
async def intro(message: Message, state: FSMContext):
    await state.clear()
    txt = 'Привет с орбиты! 🚀👽'
    await message.answer(text=txt, reply_markup=kb.main)


@router.message(F.text.lower() == 'выключить', FilterIsAdmin())
async def intro(message: Message, state: FSMContext):
    bot_activity_set(status=False)
    dp["bot_enabled"] = False
    dp_bot_enabled: bool = dp["bot_enabled"] # просто чтобы вывести на печать
    print(f"dp[\"bot_enabled\"] = {dp_bot_enabled}")
    txt = 'Бот выключен'
    await message.answer(text=txt, reply_markup=kb.main)


@router.message(F.text.lower() == 'включить', FilterIsAdmin())
async def intro(message: Message, state: FSMContext):
    bot_activity_set(status=True)
    dp["bot_enabled"] = True
    dp_bot_enabled: bool = dp["bot_enabled"] # просто чтобы вывести на печать
    print(f"dp[\"bot_enabled\"] = {dp_bot_enabled}")
    txt = 'Бот включен'
    await message.answer(text=txt, reply_markup=kb.main)


@router.message(F.text == 'Придумай салат!',
                FilterIsEnable())  # F-фильтром можно ловить всё, что пришлют, текст, медиа...
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
                       folderpath=DB_PATH + 'logs/',
                       overwrite=False
                       )
    txt = str(message.from_user.first_name) + ' получил рецепт салата'
    h(txt)
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


@router.message(F.text == "Настройки", FilterIsAdmin())
async def set_settings(message: Message):
    txt = 'Настройки для администратора'
    await message.answer(text=txt, reply_markup=kb.kb_for_admin)


@router.message(F.text == "Выключить ⭕", FilterIsAdmin())
async def set_settings_off(message: Message):
    txt = 'Бота работа остановлена.\nНо планировщик работает, фоновые задачи активны.'
    await message.answer(text=txt, reply_markup=kb.kb_for_admin)
    bot_activity_set(status=False)
    dp["bot_enabled"] = False
    dp_bot_enabled: bool = dp["bot_enabled"] # просто чтобы вывести на печать
    print(f"dp[\"bot_enabled\"] = {dp_bot_enabled}")


@router.message(F.text == 'Включить 🟢', FilterIsAdmin())
async def set_settings_on(message: Message):
    txt = 'Бота работа возобновлена будет'
    bot_activity_set(status=True)
    await message.answer(text=txt, reply_markup=kb.main)
    if scheduler.running and scheduler.state == STATE_PAUSED:
        scheduler.resume()
    dp["bot_enabled"] = True
    dp_bot_enabled: bool = dp["bot_enabled"] # просто чтобы вывести на печать
    print(f"dp[\"bot_enabled\"] = {dp_bot_enabled}")


@router.message(F.text == "Выключить и сделать дамп 🔴💾", FilterIsAdmin())
async def set_settings_off_and_dump(message: Message):
    txt = 'Бота работа остановлена будет. Дамп данных сделан будет.'
    await message.answer(text=txt, reply_markup=kb.kb_for_admin)
    bot_activity_set(status=False)
    dp["bot_enabled"] = False
    dp_bot_enabled: bool = dp["bot_enabled"] # просто чтобы вывести на печать
    print(f"dp[\"bot_enabled\"] = {dp_bot_enabled}")
    print(f'scheduler_task_running в хэндлерах: {loader.scheduler_task_running}')
    
    # Если какая-то задача выполняется и переключила флаг - ждём:
    waiting()
    
    # Останавливаем планировщик:
    scheduler.pause()
    
    # Запускаем дамп в стандартное хранилище S3:
    task_data_dump_s3()
    
    # Запускаем дамп из S3 в S3 cold:
    task_copy_all_s3_to_cold_s3()
    
    txt = 'Выполнено.\n⚠️ВНИМАНИЕ! Бот остаётся отключённым.'
    await message.answer(text=txt, reply_markup=kb.kb_for_admin)
    print(f'scheduler_task_running в хэндлерах в конце: {loader.scheduler_task_running}')


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

# @router.message()
# async def last_handler(message: Message):
#     txt = '⚠️Ой, чот сломалося... Жмите кнопки внизу экрана!'
#     await message.answer(text=txt, reply_markup=kb.main)
