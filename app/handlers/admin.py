from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.config import settings
from core.middlewares import AdminMiddleware

router = Router(name='admin')

router.message.middleware(AdminMiddleware(settings.admin))
router.callback_query.middleware(AdminMiddleware(settings.admin))


@router.message(Command('admin'))
async def cmd_admin(message: Message):
    await message.answer(text='Панель администратора', reply_markup=None)
