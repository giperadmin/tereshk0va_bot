# Пример ThrottleMiddleware:

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from time import time

class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=0.5): # В примере было <...>rate_limit=1
        self.rate_limit = rate_limit
        self.users_last_call = {}

    async def __call__(self, handler, event: TelegramObject, data):
        user_id = getattr(event.from_user, 'id', None)
        if user_id is None:
            return await handler(event, data)

        current_time = time()
        last_time = self.users_last_call.get(user_id, 0)

        if current_time - last_time < self.rate_limit:
            # Игнорируем событие или отправляем предупреждение
            if hasattr(event, 'answer'):
                await event.answer("Воу-воу! Не так быстро)", show_alert=False)
            return

        self.users_last_call[user_id] = current_time
        return await handler(event, data)

"""
И регистрируем в handlers:
from main.utils.middleware import  ThrottleMiddleware # Ограничение количества запросов от юзеров
router = Router(name='__name__')
router.message.middleware(ThrottleMiddleware(rate_limit=1.5))
router.callback_query.middleware(ThrottleMiddleware(rate_limit=1.5))
"""