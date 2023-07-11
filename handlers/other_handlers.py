from random import choice
from aiogram import Router
from aiogram.types import Message

router: Router = Router()
answers = ['Такой команды не существует',
           'Я не знаю такой команды',
           'Используйте команды из списка /help',
           'Неправильная команда, попробуйте ещё раз']


@router.message()
async def send_error_message(message: Message):
    """Responds to messages that are not provided for in the logic of the bot

    Args:
        message: class Message from TelegramObject

    Returns: function that answer with random text from "answers" list

    """
    await message.answer(choice(answers))
