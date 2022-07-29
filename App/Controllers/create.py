import http.client as code
import random

import pandas as pd
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

import App.Models.ebook as e
import App.Models.inventory as inv
from App import sys_authorize
from App.Controllers import Routes
from App.Controllers.db import engine
from App.Domain.author import Author
from App.Domain.book import Book
from App.Domain.ebook import eBook
from App.Domain.inventory import Inventory
from App.Domain.publication import Publication
from App.msgs import errmsgs

router = APIRouter()


class AuthorIn(BaseModel):
    "Author creation input."
    name: str


@router.post(Routes.CreateAuthor.value, status_code=code.CREATED.value)
@sys_authorize
async def new_author(author: AuthorIn):
    with Session(engine) as sess:
        foundauth = sess.query(Author)\
            .filter(Author.name == author.name)\
            .first()

        if foundauth:
            raise errmsgs("author", code.FORBIDDEN.value)
        else:
            newauth = Author(name=author.name)
            sess.add(newauth)
            sess.commit()
            return {"id": newauth, "detail": "Sucess creating author."}


class BookIn(BaseModel):
    "Book creation input."
    name: str
    publisher: str
    yearofpub: int
    summary: str


@router.post(Routes.CreateBook.value, status_code=code.CREATED.value)
@sys_authorize
async def new_book(author: str, book: BookIn):
    with Session(engine) as sess:
        foundauthor: Author = sess.query(Author)\
            .filter(Author.name == author)\
            .first()

        if foundauthor:
            newbook = Book(
                name=book.name,
                publisher=book.publisher,
                yearofpub=book.yearofpub,
                summary=book.summary
            )

            sess.add(newbook)
            sess.commit()

            newpub = Publication(authorid=foundauthor.id, bookid=newbook.id)

            sess.add(newpub)
            sess.commit()

            return {"id": newbook.id, "detail": "Sucess creating book."}
        else:
            raise errmsgs("author", code.NOT_FOUND.value)


class eBookIn(BaseModel):
    "eBook creation input."
    id: str
    format: e.Formats


@router.post(Routes.CreateEBook.value, status_code=code.CREATED.value)
@sys_authorize
async def new_ebook(ebook: eBookIn):

    with Session(engine) as sess:
        foundbook: Book = sess.query(Book)\
            .filter(Book.id == ebook.id)\
            .first()

        if foundbook:
            ebook = eBook(id=foundbook.id,
                          format=ebook.format)
            sess.add(ebook)
            sess.commit()
            return ebook
        else:
            raise errmsgs("book", code.NOT_FOUND.value)


class InventoryIn(BaseModel):
    "Inventory creation input."
    identifier: str
    bookid: str
    quantity: int


@router.post(Routes.CreateInventory.value, status_code=code.CREATED.value)
@sys_authorize
async def new_inventory(inventory: InventoryIn):

    with Session(engine) as sess:
        foundbook: Book = sess.query(Book)\
            .filter(Book.id == inventory.bookid)\
            .first()

        if foundbook:
            ivt = Inventory(id=inventory.identifier,
                            quantity=inventory.quantity)

            sess.add(ivt)
            sess.commit()
            return ivt
        else:
            raise errmsgs("book", code.NOT_FOUND.value)


@router.post(Routes.NewSamples.value)
@sys_authorize
async def new_samples(quantity: int):

    if not quantity:
        quantity = 10

    with Session(engine) as sess:
        df = pd.read_csv("books.csv", header=0)

        for idx in random.choices(df.index.values, k=quantity):
            row = df.iloc[idx]

            authors = []
            authornames = row["authors"].split("/")

            book = Book(
                name=row["title"],
                publisher=row["publisher"],
                yearofpub=int(row["publication_date"].split("/")[-1]),
                summary=f"Rated {row['average_rating']}."
            )

            # Add Book;
            sess.add(book)

            # Add Author;
            for author in authornames:
                foundauth = sess.query(Author)\
                    .filter_by(name=author)\
                    .first()

                if foundauth:
                    auth = foundauth
                else:
                    auth = Author(name=author)
                    sess.add(auth)

                authors.append(auth)

            sess.commit()

            ignorecurrentbook = False
            for author in authors:
                foundpub = sess.query(Publication)\
                    .filter_by(authorid=author.id, bookid=book.id)\
                    .first()

                if foundpub:
                    sess.flush()
                    sess.delete(book)
                    sess.commit()
                    ignorecurrentbook = True
                    break

                sess.add(Publication(authorid=author.id, bookid=book.id))

            if ignorecurrentbook:
                continue

            for unit in inv.units:
                if random.random() < 1 / len(inv.units):
                    sess.add(Inventory(id=unit,
                                       book_id=book.id,
                                       quantity=random.randint(0, 10)))

            if random.random() < .5:
                sess.add(
                    eBook(
                        id=book.id,
                        format=random.choice(
                            list(
                                e.Formats)).name))

            sess.commit()
        return author
