from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Придумай салат!')],
    [KeyboardButton(text='Обнулить'), KeyboardButton(text='Настройки')]
],
    resize_keyboard=True,
    input_field_placeholder='Жмите кнопки',
    one_time_keyboard=False
)

main2 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Придумай салат!')],
    [KeyboardButton(text='🔥'), KeyboardButton(text='🤢')],
    [KeyboardButton(text='Обнулить'), KeyboardButton(text='Настройки')]
],
    resize_keyboard=True,
    input_field_placeholder='Жмите кнопки',
    one_time_keyboard=False
)

main3 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Придумай салат!')],
    [KeyboardButton(text='Подобрать заправку')],
    [KeyboardButton(text='🔥'), KeyboardButton(text='🤢')],
    [KeyboardButton(text='Обнулить'), KeyboardButton(text='Настройки')]
],
    resize_keyboard=True,
    input_field_placeholder='Жмите кнопки',
    one_time_keyboard=False
)

main4 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Звездолёт🚀'), KeyboardButton(text='Салат🥗')]
],
    resize_keyboard=True,
    input_field_placeholder='Жмите кнопки',
    one_time_keyboard=False
)

kb_for_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Выключить ⭕'), KeyboardButton(text='Включить 🟢')],
    [KeyboardButton(text="Выключить и сделать дамп 🔴💾")]
],
    resize_keyboard=True,
    input_field_placeholder='Жмите кнопки',
    one_time_keyboard=False
)
