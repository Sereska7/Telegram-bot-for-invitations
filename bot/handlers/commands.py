from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import bot.core.requests as request
import bot.keyboards.main_keyboard as kb_main
from bot.core.fsm_machine.fsm_register import SetEvent
from bot.handlers.handlers_main_manu import get_schedule
from bot.keyboards.inline_keyboard import load_more, keyboard_record

router = Router()


@router.message(CommandStart())
async def start_message(message: Message):
    await request.add_user(
        tg_id=message.from_user.id,
        name=message.from_user.first_name
    )
    await message.answer(
        text="Приветсвенное сообщение",
        reply_markup=kb_main.key_main
    )


@router.callback_query(F.data.startswith('event:'))
async def choose_event(
        callback_query: CallbackQuery,
        state: FSMContext
):
    await state.update_data(event_id=int(callback_query.data.split(":")[1]))
    event = await request.get_event(int(callback_query.data.split(":")[1]))
    event_texts = []
    for text in event:
        event_text = (
            f"Title: {text['title']}\n"
            f"Description: {text["description"]}\n"
            f"Date: {text['date']}\n"
            f"Price: {text['price']}\n"
        )
        event_texts.append(event_text)
    await callback_query.message.answer(
        f"Вы выбрали:\n\n{event_texts[0]}",
        reply_markup=await keyboard_record()
    )


@router.callback_query(F.data.startswith('record'))
async def record_event(
        callback_query: CallbackQuery,
        state: FSMContext
):
    date = await state.get_data()
    user = await request.get_user_id(int(callback_query.from_user.id))
    profile = await request.get_profile_id(user_id=user)
    event = await request.get_event(event_id=int(date["event_id"]))
    record = await request.record_event(profile_id=profile.id, event_id=int(event[0]["id"]))
    await state.clear()


@router.callback_query(F.data.startswith('back'))
async def button_back(
        callback_query: CallbackQuery
):
    await get_schedule(callback_query.message, None, 0)
