from enum import Enum

from fastapi import HTTPException


class ErrorMessages(Enum):
    "Listed common error messages."

    book404 = "Book not found for given id."
    book403 = "Book is not available for deletion due to it's positive inventory."
    author404 = "Author not found for given name."
    author403 = "Attempt to create duplicate-author is not permitted."


msgs = {err.name: err.value for err in ErrorMessages}


def errmsgs(entity, code):
    "Returns the exception for the ErrorMessages enumerator."

    return HTTPException(code, msgs[str(entity) + str(code)])
