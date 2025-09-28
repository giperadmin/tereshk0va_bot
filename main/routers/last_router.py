from aiogram import Router , Bot
from aiogram.types import Message
from main import keyboards as kb




router = Router(name = '__name__')

@router.message()
async def last_handler(message: Message):
    txt = 'ЭТО ЛАСТ РОУТЕР\n⚠️Ой, чот сломалося... Жмите кнопки внизу экрана!'
    await message.answer(text=txt, reply_markup=kb.main)