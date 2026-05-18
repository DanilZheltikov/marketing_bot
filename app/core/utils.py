from typing import TypedDict

from aiogram import Bot
from aiogram.types import Message

from core.constants import MAIN_POST_EMPTY
from core.schemas import MailingStatsRead, PostRead
from keyboards.contacts import contact_keyboard


class ExtractedContent(TypedDict):
    file_id: str | None
    post_text: str | None
    content_type: str


def extract_content_from_message(message: Message) -> ExtractedContent:
    """Извлекает контент из сообщения."""
    file_id = None
    post_text = None

    match message.content_type:
        case 'photo':
            file_id = message.photo[-1].file_id
            post_text = message.caption
        case 'video':
            file_id = message.video.file_id
            post_text = message.caption
        case _:
            post_text = message.text

    return {
        'file_id': file_id,
        'post_text': post_text,
        'content_type': message.content_type
    }


async def send_post(
    bot: Bot,
    chat_id: int,
    post: PostRead | None
) -> None:
    """Отправляет пост."""

    params = {
        'chat_id': chat_id,
        'reply_markup': contact_keyboard
    }

    if post is None:
        await bot.send_message(
            text=MAIN_POST_EMPTY,
            **params
        )
        return

    match post.content_type:
        case 'photo':
            await bot.send_photo(
                photo=post.file_id,
                caption=post.post_text,
                **params
            )
        case 'video':
            await bot.send_video(
                video=post.file_id,
                caption=post.post_text,
                **params
            )
        case _:
            await bot.send_message(
                text=post.post_text,
                **params
            )


def get_mailing_stat_message(stats: MailingStatsRead) -> str:
    """Собирает из статистики строку для сообщения."""
    return (
        f'📊 *Статистика рассылки от {stats.formatted_date}*\n\n'
        f'❄️ Холодных: {stats.cold_users}\n'
        f'🚫 Заблокировали бота: {stats.bot_blocked_users}\n\n'
        f'✉️ Успешно доставленно: {stats.sucсess}'
    )
