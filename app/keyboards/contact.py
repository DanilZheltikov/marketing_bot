from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


contact_buttons = [
    [KeyboardButton(text='Поделиться контактом', request_contact=True)]
]

contact_keyboard = ReplyKeyboardMarkup(
    keyboard=contact_buttons,
    resize_keyboard=True,
    input_field_placeholder='Поделитесь, пожалуйста своим, контаком.'
)
