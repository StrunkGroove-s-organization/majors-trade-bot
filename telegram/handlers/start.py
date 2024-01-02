from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

start_message = Router()

@start_message.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}! {message}")
