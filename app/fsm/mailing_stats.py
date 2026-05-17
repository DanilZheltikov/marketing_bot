from aiogram.fsm.state import State, StatesGroup


class MailingStats(StatesGroup):
    date_mailing = State
