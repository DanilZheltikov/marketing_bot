from aiogram.fsm.state import State, StatesGroup


class MainPost(StatesGroup):
    post = State()


class WarmingPost(StatesGroup):
    choice_step_number = State()
    post = State()
