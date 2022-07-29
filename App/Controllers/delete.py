"""Delete operations

All logic on deleting books, and proper handling for inventory.

"""

import http.client as code

from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from App import sys_authorize
from App.Controllers import Routes
from App.Controllers.db import engine
from App.Domain.book import Book
from App.msgs import errmsgs

router = APIRouter()


@router.delete(Routes.DELETE_BOOK.value, status_code=code.OK.value)
@sys_authorize
async def delete_book(id: int):
    "Deletes book found with ID, if it is not w/ positive inventory."
    with Session(engine) as sess:
        foundbook = sess.query(Book)\
            .filter(Book.id == id)\
            .first()

        if foundbook:
            # Business rule & MySQL IntegrityError: prevent deleting books that are inventoried;
            # delete inventories that has quantity 0;
            if foundbook.inventories:
                for inv in foundbook.inventories:
                    if inv.quantity == 0:
                        sess.delete(inv)
                sess.commit()

            if foundbook.inventories:
                raise errmsgs("book", code.FORBIDDEN.value)
            else:
                sess.delete(foundbook)
                sess.commit()
                return {"detail": "Sucess deleting book."}

        else:
            raise errmsgs("book", code.NOT_FOUND.value)
