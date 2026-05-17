from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from core.constants import CONTACT_RECEIVED, ERROR_MESSAGE, MAIN_POST_EMPTY
from core.schemas import UserCreate
from crud_repositories.post import PostRepository
from crud_repositories.user import UsersRepository
from keyboards.contacts import contact_keyboard

router = Router(name='contacts')


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    command: CommandObject,
    user_crud: UsersRepository,
    post_crud: PostRepository
) -> None:
    await user_crud.add_user(
        UserCreate.model_validate(
            message.from_user.model_dump(),
            context={'user_role': command.args}
        )
    )
    post = await post_crud.get_main_post()

    await message.answer(
        text=MAIN_POST_EMPTY if post is None else post,
        reply_markup=contact_keyboard
    )


@router.message(F.contact)
async def handle_contact(message: Message, user_crud: UsersRepository) -> None:
    if message.contact.user_id != message.from_user.id:
        await message.answer(
            text=ERROR_MESSAGE,
            reply_markup=contact_keyboard
        )
        return
    await user_crud.set_phone_number(
        phone_number=message.contact.phone_number,
        user_id=message.from_user.id
    )
    await message.answer(
        text=CONTACT_RECEIVED,
        reply_markup=ReplyKeyboardRemove()
    )
