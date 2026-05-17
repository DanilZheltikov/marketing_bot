from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.constants import ADMIN_WELCOME_MESSAGE
from keyboards.admin import get_admin_panel_keyboard

router = Router(name='admin_panel')


@router.message(Command('admin'))
async def cmd_admin(message: Message):
    await message.answer(
        text=ADMIN_WELCOME_MESSAGE,
        reply_markup=get_admin_panel_keyboard()
    )


@router.callback_query(F.data == 'back')
async def back_to_admin_panel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text=ADMIN_WELCOME_MESSAGE,
        reply_markup=get_admin_panel_keyboard()
    )
