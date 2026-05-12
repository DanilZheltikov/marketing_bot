from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.constants import (
    ADMIN_PANEL_KEYBOARD_SIZE,
    ADD_MAIN_POST,
    EXPORT_LEADS_PHONES,
    EXPORT_ROW_SIZE,
    MAILING_CREATE,
    MAILING_EDIT_POST,
    MAILING_STATS
)


def get_admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Панель администратора."""

    builder = InlineKeyboardBuilder()
    buttons = (
        ADD_MAIN_POST,
        MAILING_CREATE,
        MAILING_EDIT_POST,
        MAILING_STATS
    )

    for text, callback_data in buttons:
        builder.button(text=text, callback_data=callback_data)

    builder.row(
        InlineKeyboardButton(
            text=EXPORT_LEADS_PHONES[0],
            callback_data=EXPORT_LEADS_PHONES[1]
        )
    )
    builder.adjust(ADMIN_PANEL_KEYBOARD_SIZE, EXPORT_ROW_SIZE)

    return builder.as_markup()
