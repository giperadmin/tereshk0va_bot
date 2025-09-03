"""возвращение случайных ответов из списков"""

from aiogram.fsm.context import FSMContext
# from ..utils import rfj # это тоже работает. Короткий импорт
from .work_with_json import read_from_json as rfj
import random
from main import DB_PATH


async def responses_to_bad_reviews(state: FSMContext) -> str:
    data = await state.get_data()
    fp = DB_PATH
    fn = 'responses.json'

    # Проверяем, что в data есть поле "remaining_responses"
    if "remaining_responses" not in data:
        all_responses = await rfj(filename=fn, folderpath=fp)
        responses = all_responses["for_negative"]
        random.shuffle(responses)
        data["remaining_responses"] = responses

    # Достаем очередной ответ
    response = data["remaining_responses"].pop()
    print(f'В списке ответов на плохие отзывы осталось {len(data["remaining_responses"])} вариантов')

    # Если ответы закончились — создаем новую перемешанную очередь
    if not data["remaining_responses"]:
        all_responses = await rfj(filename=fn, folderpath=fp)
        responses = all_responses["for_negative"]
        random.shuffle(responses)
        data["remaining_responses"] = responses

    await state.update_data(data)
    return response
