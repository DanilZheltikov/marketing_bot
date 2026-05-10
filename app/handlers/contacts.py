from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from core.database import Repositories
from core.schemas import ContactCreate

router = Router(name='contacts')


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    command: CommandObject,
    repositories: Repositories
) -> None:
    await repositories.contacts.add_contact(
        ContactCreate.model_validate(
            message.from_user,
            context={'user_role': command.args}
        )
    )
    await message.answer(text='Пока просто текст', reply_markup=None)


@router.message(F.contact)
async def handle_contact(message: Message, repositories: Repositories) -> None:
    if message.contact.user_id != message.from_user.id:
        await message.answer(
            text='Отправьте, пожалуйста, свой контакт, через кнопку в меню'
        )
        return
    await repositories.contacts.add_phone_number_to_contact(
        phone_number=message.contact.phone_number,
        user_id=message.from_user.id
    )
    await message.answer(
        text='Снова просто текст',
        reply_markup=ReplyKeyboardRemove()
    )
