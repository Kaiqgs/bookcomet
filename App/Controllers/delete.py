from App import sys_authorize
from App.Domain.book import Book
from App.Controllers.db import engine


from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from App.msgs import errmsgs

router = APIRouter()


@router.delete("/delete-book/{id}", status_code=200)
@sys_authorize
async def delete_book(id: int):
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
                raise errmsgs("book", 403)
            else:
                sess.delete(foundbook)
                sess.commit()
                return {"detail": "Sucess deleting book."}

        else:
            raise errmsgs("book", 404)
