from aiogram.fsm.state import State, StatesGroup


class MailingStatsStates(StatesGroup):
    date_mailing = State()
