from aiogram import Router
from aiogram import F
from aiogram.types import Message, CallbackQuery

router = Router()

# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
# @router.message()
# async def send_echo(message: Message):
#     await message.answer(f'Это эхо! {message.text}')
