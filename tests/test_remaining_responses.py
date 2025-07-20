import random
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


@router.message()
async def handle_message(message: Message, state: FSMContext):
    data = await state.get_data()

    # Инициализируем или обновляем очередь пользователя
    if "remaining_responses" not in data:
        responses = ["Ответ 1", "Ответ 2", "Ответ 3", "Ответ 4", "Ответ 5", "Ответ 6", "Ответ 7"]
        random.shuffle(responses)
        data["remaining_responses"] = responses

    # Достаем очередной ответ
    response = data["remaining_responses"].pop()

    # Если ответы закончились — создаем новую перемешанную очередь
    if not data["remaining_responses"]:
        responses = ["Ответ 1", "Ответ 2", "Ответ 3", "Ответ 4", "Ответ 5", "Ответ 6", "Ответ 7"]
        random.shuffle(responses)
        data["remaining_responses"] = responses

    await state.update_data(data)
    await message.answer(response)

