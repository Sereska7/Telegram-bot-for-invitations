from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import bot.core.requests as request
from bot.core.fsm_machine.fsm_register import SetEvent, CodePerson
from bot.keyboards.inline_keyboard import load_more


router = Router()


@router.message(F.text == "Расписание")
async def get_schedule(
        message: Message,
        state: FSMContext,
        offset: int = 0,
):
    events = await request.get_events(offset)
    if not events:
        await message.answer(text="No events found.")

    event_texts = []
    for event in events:
        event_text = (
            f"Title: {event['title']}\n"
            f"Date: {event['date']}\n"
            f"Price: {event['price']}\n"
        )
        event_texts.append(event_text)
    full_text = "\n".join(event_texts)
    if full_text.strip():
        await message.answer(
            text=full_text,
            reply_markup=await load_more(offset=offset)
        )
    if isinstance(state, FSMContext):
        await state.set_state(SetEvent.event_id)


@router.callback_query(F.data.startswith('load_more:'))
async def load_more_events(callback_query: CallbackQuery):
    offset = int(callback_query.data.split(":")[1])
    await get_schedule(callback_query.message, None, offset)
    await callback_query.answer()


@router.message(F.text == "Мой профиль")
async def send_profile(
        message: Message
):
    user = await request.get_user_id(message.from_user.id)
    profile = await request.get_profile(user_id=user)
    result = []
    for object_profile in profile:
        profile_text = (
            f"Имя: {object_profile['first_name']}\n"
            f"Фамилия: {object_profile['last_name']}\n"
            f"Телефон: {object_profile['phone_number']}\n"
            f"Должность: {object_profile["position"]}\n"
            f"Уникальный код: {object_profile["unique_id"]}"
        )
        result.append(profile_text)
    text_profile = "".join(result)
    await message.answer(f"Ваши данный:\n\n{text_profile}")


@router.message(F.text == "Мои мероприятия")
async def get_my_records(message: Message):
    user = await request.get_user_id(message.from_user.id)
    profile = await request.get_profile_id(user)
    records = await request.get_records(profile.id)
    events = []
    for record in records:
        events.append(int(record["event_id"]))
    event_texts = []
    for i in events:
        event = await request.get_event(int(i))
        for one in event:
            event_text = (
                f"Title: {one['title']}\n"
                f"Date: {one['date']}\n"
                f"Price: {one['price']}\n"
            )
            event_texts.append(event_text)
    full_text = "\n".join(event_texts)
    await message.answer(text=full_text)


@router.message(F.text == "Знакомства")
async def look_for_person(
        message: Message,
        state: FSMContext
):
    await message.answer(text="Введите код пользователя")
    await state.set_state(CodePerson.code)


@router.message(CodePerson.code)
async def get_person(
        message: Message,
        state: FSMContext
):

    await state.update_data(code=message.text)
    date = await state.get_data()
    print(date)
    un_code = date["code"]
    profile_person = await request.get_profile_by_code(int(un_code))
    if not profile_person:
        await message.answer(text="Пользователь не найден")
    else:
        result = []
        for object_profile in profile_person:
            profile_text = (
                f"Имя: {object_profile['first_name']}\n"
                f"Фамилия: {object_profile['last_name']}\n"
                f"Телефон: {object_profile['phone_number']}\n"
                f"Должность: {object_profile["position"]}\n"
                f"Уникальный код: {object_profile["unique_id"]}"
            )
            result.append(profile_text)
        text_profile = "".join(result)
        await message.answer(f"Данные пользователя:\n\n{text_profile}")
