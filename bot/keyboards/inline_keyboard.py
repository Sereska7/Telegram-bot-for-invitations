from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.requests import get_events, get_records


async def load_more(offset):
    events = await get_events(offset=offset)
    keyboard = InlineKeyboardBuilder()
    for event in events:
        keyboard.add(
            InlineKeyboardButton(
                text=event["title"], callback_data=f"event:{event["id"]}"
            )
        )
    keyboard.add(
        InlineKeyboardButton(text="Load more", callback_data=f"load_more:{offset + 2}")
    )
    return keyboard.adjust(2).as_markup()


async def keyboard_record():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Записаться", callback_data="record"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back"))
    return keyboard.adjust(2).as_markup()


async def load_more_my_events(offset: int = 0):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Load more", callback_data=f"load_events:{offset + 2}"
        )
    )
    return keyboard.adjust(2).as_markup()


async def button_reload():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Ввести другой код", callback_data="reload_code")
    )
    return keyboard.as_markup()
