from aiogram.filters import BaseFilter
from aiogram.types import Message
from main import ADMIN_TG_ID
from main.loader import dp

class FilterIsAdmin(BaseFilter):
    print('сработал FilterIsAdmin')
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == ADMIN_TG_ID

class FilterIsEnable(BaseFilter):
    print('сработал FilterIsEnable')
    print(f"печать из фильтра FilterIsEnable: dp[\"bot_enabled\"] = {dp["bot_enabled"]}")
    async def __call__(self, message: Message) -> bool:
        return dp["bot_enabled"]