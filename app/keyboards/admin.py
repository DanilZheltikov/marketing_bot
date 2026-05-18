from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.callbacks import MailingDateCallback
from core.constants import (
    ADMIN_PANEL_KEYBOARD_SIZE,
    ADD_MAIN_POST,
    BACK,
    CHOICE_KEYBOARD_SIZE,
    EXPORT_LEADS_PHONES,
    EXPORT_ROW_SIZE,
    FIRST_STEP,
    MAILING_POST,
    MAILING_STATS,
    STEPS_COUNT
)
from core.schemas import MailingStatsDate

BACK_TO_ADMIN_PANEL_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=BACK[0], callback_data=BACK[1])]
    ]
)


def get_admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Панель администратора."""

    builder = InlineKeyboardBuilder()
    buttons = (
        ADD_MAIN_POST,
        MAILING_POST,
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


def get_choice_warming_post_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора шага прогревающего поста."""

    builder = InlineKeyboardBuilder()

    for step_number in range(FIRST_STEP, FIRST_STEP + STEPS_COUNT):
        builder.button(
            text=f'{step_number}',
            callback_data=f'step_{step_number}'
        )
    builder.adjust(CHOICE_KEYBOARD_SIZE)
    builder.attach(
        InlineKeyboardBuilder.from_markup(BACK_TO_ADMIN_PANEL_KEYBOARD)
    )
    return builder.as_markup()


def get_choice_mailing_date_keyboard(
    mailing_dates: list[MailingStatsDate]
) -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора даты рассылки."""

    if not mailing_dates:
        return BACK_TO_ADMIN_PANEL_KEYBOARD

    builder = InlineKeyboardBuilder()
    builder.attach(
        InlineKeyboardBuilder.from_markup(BACK_TO_ADMIN_PANEL_KEYBOARD)
    )
    for mailing_date in mailing_dates:
        builder.button(
            text=mailing_date.formatted_date,
            callback_data=MailingDateCallback(id=mailing_date.id)
        )
    return builder.as_markup()
