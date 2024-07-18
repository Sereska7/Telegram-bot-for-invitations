from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import bot.core.requests as request
import bot.core.utils as util
from bot.core.fsm_machine.fsm_condition import RegisterProfileState
from bot.core.utils import generate_unique_code


router = Router()


@router.message(F.text == "Зарегистрироваться")
async def start_register(message: Message, state: FSMContext):
    user = await request.get_user_id(message.from_user.id)
    profile = await request.get_profile(user_id=user)
    if not profile:
        await state.set_state(RegisterProfileState.first_name)
        await message.reply("Привет! Давай начнем регистрацию. Как тебя зовут?")
    else:
        list_texts = await util.conversion_to_text_for_profile(profile)
        text_profile = "".join(list_texts)
        await message.answer(
            f"Вы уже зарегистрированны\n\nВаши данный:\n{text_profile}"
        )


@router.message(RegisterProfileState.first_name)
async def register_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(RegisterProfileState.last_name)
    await message.answer("Теперь, напиши свою фамилию")


@router.message(RegisterProfileState.last_name)
async def register_last_number(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(RegisterProfileState.phone_number)
    await message.answer("Теперь. Напиши свои номер телефона")


@router.message(RegisterProfileState.phone_number)
async def register_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(RegisterProfileState.position)
    await message.answer("Теперь. Напиши свою должность")


@router.message(RegisterProfileState.position)
async def register_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    date = await state.get_data()
    user_id = await request.get_user_id(message.from_user.id)
    unique_id = await generate_unique_code()
    result = await request.create_profile(
        user_id=user_id,
        first_name=date["first_name"],
        last_name=date["last_name"],
        phone_number=date["phone_number"],
        position=date["position"],
        unique_id=unique_id,
    )
    await message.answer(text=result)
    await state.clear()
