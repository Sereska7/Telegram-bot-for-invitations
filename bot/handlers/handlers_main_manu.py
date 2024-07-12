from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import bot.core.requests as request
import bot.core.utils as util
from bot.core.fsm_machine.fsm_condition import SetEvent, CodePerson, UserID
from bot.keyboards.inline_keyboard import load_more, load_more_my_events, button_reload

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

    list_texts = await util.conversion_to_text_for_events_min(events)
    full_text = "\n".join(list_texts)
    if full_text.strip():
        await message.answer(
            text=full_text, reply_markup=await load_more(offset=offset)
        )
    if isinstance(state, FSMContext):
        await state.set_state(SetEvent.event_id)


@router.callback_query(F.data.startswith("load_more:"))
async def load_more_events(callback_query: CallbackQuery):
    offset = int(callback_query.data.split(":")[1])
    await get_schedule(callback_query.message, None, offset)
    await callback_query.answer()


@router.message(F.text == "Мой профиль")
async def send_profile(message: Message):
    user = await request.get_user_id(message.from_user.id)
    profile = await request.get_profile(user_id=user)
    list_texts = await util.conversion_to_text_for_profile_by_userid(profile)
    text_profile = "".join(list_texts)
    await message.answer(f"Ваши данный:\n\n{text_profile}")


@router.message(F.text == "Мои мероприятия")
async def get_my_records(message: Message, user_tg_id: int = None, offset: int = 0):
    user = await request.get_user_id(message.from_user.id if not user_tg_id else user_tg_id)
    profile = await request.get_profile_id(user)
    records = await request.get_records(profile.id, offset)
    events = []
    for record in records:
        events.append(int(record["event_id"]))
    list_texts = await util.conversion_to_text_for_event_id_min(events)
    full_text = "\n".join(list_texts)
    if full_text.strip():
        await message.answer(text=full_text, reply_markup=await load_more_my_events(offset))
    else:
        await message.answer(text="No events found.")


@router.callback_query(F.data.startswith("load_events:"))
async def more_my_events(callback_query: CallbackQuery):
    offset = int(callback_query.data.split(":")[1])
    user_tg_id = int(callback_query.from_user.id)
    await get_my_records(callback_query.message, user_tg_id, offset)
    await callback_query.answer()


@router.message(F.text == "Знакомства")
async def look_for_person(message: Message, state: FSMContext):
    await message.answer(text="Введите код пользователя")
    await state.set_state(CodePerson.code)


@router.message(CodePerson.code)
async def get_person(message: Message, state: FSMContext):
    code = message.text
    if len(code) == 4:
        if code.isdigit():
            await state.update_data(code=message.text)
            date = await state.get_data()
            un_code = date["code"]
            profile_person = await request.get_profile_by_code(int(un_code))
            if not profile_person:
                await message.answer(text="Пользователь не найден", reply_markup=await button_reload())
            else:
                list_texts = await util.conversion_to_text_for_profile(profile_person)
                text_profile = "".join(list_texts)
                await message.answer(f"Данные пользователя:\n\n{text_profile}")
    else:
        await message.answer(text="Вы ввели код не корректно\nПовторите попытку")
        await look_for_person(message, state)


@router.callback_query(F.data.startswith("reload_code"))
async def reload_code(callback_query: CallbackQuery, state: FSMContext):
    await look_for_person(callback_query.message, state)


