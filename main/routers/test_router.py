from aiogram import Router , Bot, F
from aiogram.types import Message
from main import keyboards as kb
from main.utils.filters import FilterIsAdmin
from main.utils.history_utils import add_to_history
from main.loader import dp



router = Router(name = '__name__')

@router.message(F.text=='TEST', FilterIsAdmin())
async def last_handler(message: Message):
    txt = f"dp[\"bot_enabled\"] = {dp["bot_enabled"]}"
    add_to_history('нажата кнопка TEST: '+ txt)
    await message.answer(text=txt, reply_markup=kb.main)
    
