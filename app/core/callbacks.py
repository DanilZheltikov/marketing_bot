from aiogram.filters.callback_data import CallbackData


class MailingDateCallback(CallbackData, prefix='dates'):
    id: int
