"""Update operations

Update book functionality, with optional overriding.
"""

import http.client as code
from typing import Union

from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from App import sys_authorize
from App.Controllers import Routes
from App.Controllers.db import engine
from App.Domain.book import Book
from App.msgs import errmsgs

router = APIRouter()


class UpdateBookIn(BaseModel):
    "Book update input."
    name: Union[str, None]
    publisher: Union[str, None]
    yearofpub: Union[int, None]
    summary: Union[str, None]


@router.put(Routes.UPDATE_BOOK.value)
@sys_authorize
async def update_book(id: int, updtbook: UpdateBookIn):
    """
    Update ID book with UpdateBookInput;
    """

    with Session(engine) as sess:
        foundbook = sess.query(Book)\
            .filter(Book.id == id)\
            .first()

        if foundbook:
            foundbook.name = foundbook.name if updtbook.name is None \
                else updtbook.name

            foundbook.publisher = foundbook.publisher if updtbook.publisher is None \
                else updtbook.publisher

            foundbook.yearofpub = foundbook.yearofpub if updtbook.yearofpub is None \
                else updtbook.yearofpub

            foundbook.summary = foundbook.summary if updtbook.summary is None \
                else updtbook.summary

            sess.commit()

            return foundbook

        else:
            raise errmsgs("book", code.NOT_FOUND.value)
