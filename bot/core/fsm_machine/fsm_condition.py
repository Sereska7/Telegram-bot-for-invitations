from aiogram.fsm.state import State, StatesGroup


class RegisterProfileState(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    position = State()


class SetEvent(StatesGroup):
    event_id = State()


class CodePerson(StatesGroup):
    code = State()


class UserID(StatesGroup):
    user_tg_id = State()
