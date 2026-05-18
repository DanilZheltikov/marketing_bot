from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.callbacks import PostStepCallback
from core.constants import (
    ADMIN_CHOICE_STEP_MESSAGE,
    ADMIN_CONFIRM_MESSAGE,
    ADMIN_WRITE_POST_MESSAGE,
    MAIN_POST_NUMBER
)
from core.schemas import PostCreate
from core.utils import extract_content_from_message
from crud_repositories.post import PostRepository
from fsm.post import MainPost, WarmingPost
from keyboards.admin import (
    BACK_TO_ADMIN_PANEL_KEYBOARD,
    get_choice_warming_post_keyboard
)

router = Router()


@router.callback_query(F.data == 'add_main_post')
async def process_main_post(callback: CallbackQuery, state: FSMContext):
    """
    Устанавливает состояние ожидания текста главного поста и обновляет меню.
    """
    await state.set_state(MainPost.post)
    await callback.message.edit_text(
        text=ADMIN_WRITE_POST_MESSAGE,
        reply_markup=BACK_TO_ADMIN_PANEL_KEYBOARD
    )


@router.message(MainPost.post)
async def add_main_post(
    message: Message,
    state: FSMContext,
    post_crud: PostRepository
):
    """Сохраняет главный пост в базу данных и уведомляет об успехе."""

    await post_crud.add_post(
        PostCreate(
            main_post=True,
            step_number=MAIN_POST_NUMBER,
            **extract_content_from_message(message)
        )
    )
    await state.clear()
    await message.answer(
        text=ADMIN_CONFIRM_MESSAGE,
        reply_markup=BACK_TO_ADMIN_PANEL_KEYBOARD
    )


@router.callback_query(F.data == 'mailing_post')
async def process_сhoise_step_warming_post(
    callback: CallbackQuery,
    state: FSMContext
):
    """
    Переводит в режим выбора шага прогрева и отображает клавиатуру этапов.
    """
    await state.set_state(WarmingPost.step_number)
    await callback.message.edit_text(
        text=ADMIN_CHOICE_STEP_MESSAGE,
        reply_markup=get_choice_warming_post_keyboard()
    )
    await callback.answer()


@router.callback_query(
        PostStepCallback.filter(),
        WarmingPost.step_number
    )
async def process_warming_post_writing(
    callback: CallbackQuery,
    callback_data: PostStepCallback,
    state: FSMContext
):
    """Фиксирует номер шага прогрева и запрашивает текст сообщения."""

    await state.update_data(step=callback_data.step)
    await state.set_state(WarmingPost.post)
    await callback.message.edit_text(
        text=ADMIN_WRITE_POST_MESSAGE,
        reply_markup=BACK_TO_ADMIN_PANEL_KEYBOARD
    )
    await callback.answer()


@router.message(WarmingPost.post)
async def add_warming_post(
    message: Message,
    state: FSMContext,
    post_crud: PostRepository
):
    """
    Сохраняет прогревочный пост для выбранного шага и подтверждает сохранение.
    """
    post_data = await state.get_data()

    await post_crud.add_post(
        PostCreate(
            step_number=post_data['step'],
            **extract_content_from_message(message)
        )
    )
    await state.clear()

    await message.answer(
        text=ADMIN_CONFIRM_MESSAGE,
        reply_markup=BACK_TO_ADMIN_PANEL_KEYBOARD
    )
