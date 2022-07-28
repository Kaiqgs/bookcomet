from App import sys_authorize
from App.Domain.book import Book
from App.Controllers.db import engine
from App.msgs import errmsgs

from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from typing import Union

router = APIRouter()


class UpdateBookIn(BaseModel):
    name: Union[str, None]
    publisher: Union[str, None]
    yearofpub: Union[int, None]
    summary: Union[str, None]


@router.put("/update-book/{bookid}")
@sys_authorize
async def list_books(bookid: int, updtbook: UpdateBookIn):
    with Session(engine) as sess:
        foundbook = sess.query(Book)\
            .filter(Book.id == bookid)\
            .first()

        if foundbook:

            foundbook.name = foundbook.name if updtbook.name is None else updtbook.name
            foundbook.publisher = foundbook.publisher if updtbook.publisher is None else updtbook.publisher
            foundbook.yearofpub = foundbook.yearofpub if updtbook.yearofpub is None else updtbook.yearofpub
            foundbook.summary = foundbook.summary if updtbook.summary is None else updtbook.summary
            sess.commit()
            
            return foundbook

        else:
            raise errmsgs("book", 404)
