from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.constants import (
    ADMIN_CHOICE_STEP_MESSAGE,
    ADMIN_CONFIRM_MESSAGE,
    ADMIN_WRITE_POST_MESSAGE
)
from fsm.post import MainPost, WarmingPost
from keyboards.admin import BACK_TO_ADMIN_PANEL_KEYBOARD

router = Router()


@router.callback_query(F.data == 'add_main_post')
async def process_main_post(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MainPost.post)
    await callback.message.edit_text(
        text=ADMIN_WRITE_POST_MESSAGE,
        reply_markup=BACK_TO_ADMIN_PANEL_KEYBOARD
    )


@router.message(MainPost.post)
async def add_main_post(message: Message, state: FSMContext):
    await message.edit_text(
        text=ADMIN_CONFIRM_MESSAGE,
        reply_markup=BACK_TO_ADMIN_PANEL_KEYBOARD
    )


@router.callback_query(F.data == 'mailing_post')
async def process_warming_post(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WarmingPost.choice_step_number)
    await callback.message.edit_text(
        text=ADMIN_CHOICE_STEP_MESSAGE
    )
