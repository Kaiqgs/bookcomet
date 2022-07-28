

from App import sys_authorize
from App.Domain.book import Book
from App.Domain.author import Author
from App.Domain.publication import Publication
from App.Controllers.db import engine

from sqlalchemy.orm import Session
from fastapi import Response
from fastapi.routing import APIRouter
from fastapi.encoders import jsonable_encoder
import json
from typing import Union

router = APIRouter()


@router.get("/list-books/")
@sys_authorize
async def list_books(bookname: Union[str, None] = None,
                     authorname: Union[str, None] = None,
                     publisher: Union[str, None] = None,
                     limit: int = 10):
    with Session(engine) as sess:
        bquery = sess.query(Book)

        if bookname is not None:
            bquery = bquery.filter(Book.name.like(bookname))
        if publisher is not None:
            bquery = bquery.filter(Book.publisher.like(publisher))

        if authorname is not None:
            authors = sess.query(Author)\
                .filter(Author.name.like(authorname))\
                .all()

            authorids = [a.id for a in authors]

            bquery = bquery.join(Publication)\
                .filter(Publication.authorid.in_(authorids))

        books = bquery.limit(limit).all()

        jdict = jsonable_encoder(books)
        book: Book
        for book, dictobj in zip(books, jdict):
            for key, value in book.relations.items():
                dictobj[key] = jsonable_encoder(value)

        jdump = json.dumps(jdict)

        return Response(media_type="application/json", content=jdump)
