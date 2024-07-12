from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


key_main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Расписание")],
                                         [KeyboardButton(text="Зарегистрироваться")],
                                         [KeyboardButton(text="Мои мероприятия")],
                                         [KeyboardButton(text="Мой профиль")],
                                         [KeyboardButton(text="Знакомства"),
                                          KeyboardButton(text="FAQ")]],
                               resize_keyboard=True
                               )
