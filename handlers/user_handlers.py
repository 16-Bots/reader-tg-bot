from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book, BOOK_LENGTH

router: Router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(LEXICON['/start'])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(LEXICON['/help'])


@router.message(Command(commands=['beginning']))
async def beginning_command(message: Message):
    user_id = message.from_user.id
    users_db[user_id]["page"] = 1
    text = book[users_db[user_id]["page"]]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(user_id)
    )


@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(message.from_user.id))


@router.message(Command(commands='bookmarks'))
async def bookmarks_command(message: Message):
    """Show added bookmarks

    Args:
        message: class Message from TelegramObject

    Returns: function that responds to the user with a bookmark
            keyboard if it's not empty, otherwise with a warning text

    """
    if users_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]["bookmarks"]))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(Text(text=['forward', 'backward']))
async def forward_backward_command(callback: CallbackQuery):
    """Move a page forward or back

    Args:
        callback: class CallbackQuery from TelegramObject

    Returns: function that directs the user to the previous or next page

    """
    shift = 1 if callback.data == 'forward' else -1
    user_id = callback.from_user.id
    users_db[user_id]["page"] += shift
    text = book[users_db[user_id]["page"]]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(user_id)
    )


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки!')


@router.callback_query(IsDigitCallbackData())
async def bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(callback.from_user.id)
    )
    await callback.answer()


@router.callback_query(Text(text='edit_bookmarks'))
async def edit_bookmark_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(*users_db[callback.from_user.id]["bookmarks"]))
    await callback.answer()


@router.callback_query(Text(text='cancel'))
async def cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


@router.callback_query(IsDelBookmarkCallbackData())
async def del_bookmark_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3]))
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *users_db[callback.from_user.id]["bookmarks"])
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()


@router.message(Command(commands='goto'))
async def goto_command(message: Message):
    """Go to some page

    Args:
        message: class Message from TelegramObject

    Returns: function that directs user to the requested page

    """
    try:
        users_db[message.from_user.id]["page"] = int(message.text[6:len(message.text)])
        text = book[users_db[message.from_user.id]["page"]]
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(message.from_user.id)
        )
    except (ValueError, KeyError):
        await message.answer(f'Введите номер страницы от 1 до {BOOK_LENGTH}'
                             f' через пробел после команды /goto (пример: /goto 1)')
