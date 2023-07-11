import os

BOOK_PATH = 'book/Master_and_Margarita.txt'
PAGE_SIZE = 1000

book: dict[int, str] = {}


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    """Return string with text and it`s size

    Args:
        text: given text
        start: start position
        size: required size

    Returns: tuple with string and integer values - text of the given page and it`s size

    """
    end_signs = ',.!:;?'
    counter = 0
    if len(text) < start + size:
        size = len(text) - start
        text = text[start:start + size]
    else:
        if text[start + size] == '.' and text[start + size - 1] in end_signs:
            text = text[start:start + size - 2]
            size -= 2
        else:
            text = text[start:start + size]
        for i in range(size - 1, 0, -1):
            if text[i] in end_signs:
                break
            counter = size - i
    page_text = text[:size - counter]
    page_size = size - counter
    return page_text, page_size


def prepare_book(path: str) -> None:
    """Form book dictionary to show text in comfortable format

    Args:
        path: path to the book

    Returns: None

    """
    with open(path, 'r') as file:
        text = file.read()
    start, page_number = 0, 1
    while start < len(text):
        page_text, page_size = _get_part_text(text, start, PAGE_SIZE)
        start += page_size
        book[page_number] = page_text.strip()
        page_number += 1


prepare_book(os.path.join(os.getcwd(), BOOK_PATH))
BOOK_LENGTH: int = len(book)
