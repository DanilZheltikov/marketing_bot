from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.callbacks import MailingDateCallback
from core.constants import MAILING_STATS_MESSAGE
from core.utils import get_mailing_stat_message
from crud_repositories.mailing_stats import MailingStatsRepository
from fsm.mailing_stats import MailingStatsStates
from keyboards.admin import (
    BACK_TO_ADMIN_PANEL_KEYBOARD,
    get_choice_mailing_date_keyboard
)

router = Router()


@router.callback_query(F.data == 'mailing_stats')
async def process_mailing_stats(
    callback: CallbackQuery,
    state: FSMContext,
    mailing_stats_crud: MailingStatsRepository
):
    """Выводит список дат рассылок и переключает FSM на выбор даты."""

    mailing_dates = await mailing_stats_crud.get_dates_from_mailing_stats()

    await callback.message.edit_text(
        text=MAILING_STATS_MESSAGE,
        reply_markup=get_choice_mailing_date_keyboard(
            mailing_dates=mailing_dates
        )
    )
    await state.set_state(MailingStatsStates.date_mailing)


@router.callback_query(
    MailingDateCallback.filter(),
    MailingStatsStates.date_mailing
)
async def get_mailing_stats(
    callback: CallbackQuery,
    callback_data: MailingDateCallback,
    state: FSMContext,
    mailing_stats_crud: MailingStatsRepository
):
    """Получает статистику по ID из колбэка и выводит её пользователю."""
    stats = await mailing_stats_crud.get_mailing_stats(
        mailing_stats_id=callback_data.id
    )
    await state.clear()

    await callback.message.edit_text(
        text=get_mailing_stat_message(stats),
        reply_markup=BACK_TO_ADMIN_PANEL_KEYBOARD
    )
