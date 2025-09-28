from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from typing import Callable, Awaitable, Dict, Any
import json
from time import time
from main import ADMIN_TG_ID
# from main.loader import dp # todo
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

# from main.loader import dp

from main.utils.bot_activity_get import bot_activity_get


# from main import FilterIsAdmin as IsAdmin


class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=1):  # В примере было <...>rate_limit=1
        self.rate_limit = rate_limit
        self.users_last_call = {}

    async def __call__(self, handler, event: TelegramObject, data):
        # user_id = getattr(event.from_user, 'id', None)
        # if user_id is None:
        #     return await handler(event, data)
        print(f"Сработал ThrottleMiddleware")
        from_user = None
        message_or_callback = None

        if event.message:
            from_user = event.message.from_user
            message_or_callback = event.message
        elif event.callback_query:
            from_user = event.callback_query.from_user
            message_or_callback = event.callback_query
        elif event.inline_query:
            from_user = event.inline_query.from_user
        elif event.chosen_inline_result:
            from_user = event.chosen_inline_result.from_user
        elif event.my_chat_member:
            from_user = event.my_chat_member.from_user
        elif event.chat_member:
            from_user = event.chat_member.from_user
        elif event.message_reaction:
            from_user = event.message_reaction.user
        # ⚠️ можно дописать сюда и другие типы апдейтов, при необходимости

        # если нет юзера - пропускаем
        if not from_user:
            return await handler(event, data)

        user_id = from_user.id

        # print(user_id)

        current_time = time()
        last_time = self.users_last_call.get(user_id, 0)

        if current_time - last_time < self.rate_limit:
            # Игнорируем событие или отправляем предупреждение
            if message_or_callback:
                try:
                    if hasattr(message_or_callback, "answer"):
                        await message_or_callback.answer("Воу-воу! Не так быстро) 🚦")
                except Exception as e:
                    # print(f"Не смогли отправить предупреждение: {e}")
                    pass
            return

        self.users_last_call[user_id] = current_time
        return await handler(event, data)


class CheckBotActivity(BaseMiddleware):
    """Проверяем, что бот активен"""
    def __init__(self, filepath: str):
        self.filepath = filepath

    async def __call__(
        self,
        handler: Callable[[Dict[str, Any], Any], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:

        print('сработал class CheckBotActivity(BaseMiddleware):')
        print(f'self.filepath = {str(self.filepath)}')

        # читаем файл на каждый апдейт
        with open(self.filepath, "r", encoding="utf-8") as f:
            bot_status = json.load(f)
        # print(bot_status)

        # bot_enabled = dp.get("dp_bot_enabled", True)

        user = event.message.from_user
        user_id = user.id

        if user_id == ADMIN_TG_ID:
            # print ('IsAdmin = ',str(IsAdmin))
            return await handler(event, data)

        if not bot_status.get("bot_enabled", True):
            # if not bot_enabled:
            await event.message.answer("Бот сейчас выключен ❌")
            return  # если бот "выключен" — игнорим апдейт

        return await handler(event, data)

    # print("=== CheckBotActivity сработал  ===")
    # print(f"Тип события: {type(event)}")
    # folderpath = 'main/config/'
    # filename = 'bot_activity.json'
    # print(f'{folderpath}{filename}')
    # with open(f'{folderpath}{filename}', 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    # print (data)
    # bot_enabled = data.get('bot_enabled',True)
    # print(bot_enabled)
    # data={}
    #
    # # Можно сохранить данные для всех обработчиков
    # # data["outer_info"] = "Injected by OuterMiddleware"
    #
    # if bot_enabled:
    #     return await handler(event, data)
    # return return await handler(event, data)


"""
И регистрируем в handlers:
from main.utils.middleware import  ThrottleMiddleware # Ограничение количества запросов от юзеров
router = Router(name='__name__')
router.message.middleware(ThrottleMiddleware(rate_limit=1.5))
router.callback_query.middleware(ThrottleMiddleware(rate_limit=1.5))
"""

"""
В aiogram 3.x есть два типа middleware:

1. inner — вешаются на конкретный роутер 
(через router.message.middleware(...), router.callback_query.middleware(...) и т.д.).
Они выполняются внутри контекста этого роутера.

2. outer — вешаются на весь Dispatcher (через dp.update.outer_middleware(...)).
Они срабатывают самыми первыми, ещё до того, как начнётся разбор апдейта по роутерам и фильтрам.

КАК ПОДКЛЮЧИТЬ:

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command


bot = Bot("YOUR_BOT_TOKEN")
dp = Dispatcher()

# Подключаем OUTER middleware на все апдейты
dp.update.outer_middleware(OuterMiddleware())


@dp.message(Command("start"))
async def cmd_start(message: Message, outer_info: str):
    await message.answer(f"Привет! Outer middleware сказал: {outer_info}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))

"""
