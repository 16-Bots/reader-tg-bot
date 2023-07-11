from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.file_handling import BOOK_LENGTH
from database.database import users_db


def pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons])
    return kb_builder.as_markup()


def create_pagination_keyboard(user_id):
    page: int = users_db[user_id]["page"]
    backward_button = 'backward'
    middle_button = f'{page}/{BOOK_LENGTH}'
    forward_button = 'forward'
    if page == 1:
        return pagination_keyboard(middle_button, forward_button)
    elif 1 < page < BOOK_LENGTH:
        return pagination_keyboard(backward_button,
                                   middle_button,
                                   forward_button)
    else:
        return pagination_keyboard(backward_button, middle_button)
