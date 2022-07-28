from fastapi import HTTPException
from enum import Enum


class ErrorMessages(Enum):
    book404 = "Book not found for given id."
    book403 = "Book is not available for deletion due to it's positive inventory."
    author404 = "Author not found for given name."
    author403 = "Attempt to create duplicate-author is not permitted."


msgs = {err.name: err.value for err in ErrorMessages}


def errmsgs(entity, code):
    return HTTPException(code, msgs[str(entity) + str(code)])
