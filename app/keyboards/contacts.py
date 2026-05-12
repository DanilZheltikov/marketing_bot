from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from core.constants import REQUEST_CONTACT, REQUEST_CONTACT_PLACEHOLDER


contact_buttons = [
    [KeyboardButton(text=REQUEST_CONTACT, request_contact=True)]
]

contact_keyboard = ReplyKeyboardMarkup(
    keyboard=contact_buttons,
    resize_keyboard=True,
    input_field_placeholder=REQUEST_CONTACT_PLACEHOLDER
)
