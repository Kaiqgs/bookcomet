import sqlalchemy as sqa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from App.Domain import Base
from App.Domain.publication import Publication
from App.Models.book import IBook


class Book(Base, IBook):
    """
    Book entity ORM mapped.
    """

    __tablename__ = "books"
    id = sqa.Column(sqa.Integer, primary_key=True)
    name = sqa.Column(sqa.String(256))

    publisher = sqa.Column(sqa.String(256))
    yearofpub = sqa.Column(sqa.Integer)
    summary = sqa.Column(sqa.String(512))

    authors = relationship("Author",
                           secondary=Publication.__table__,
                           back_populates="releases")

    inventories = relationship("Inventory",
                               back_populates="book")

    digital = relationship("eBook",
                           back_populates="book",
                           cascade="all, delete-orphan")

    @hybrid_property
    def relations(self) -> dict:
        "Book non direct relationships."
        return {"authors": self.authors,
                "inventories": self.inventories,
                "digital": self.digital}

    def __repr__(self) -> str:
        return f"<Book[{self.id:03d}]: {self.name} w/ {self.publisher} @ {self.yearofpub:04d}>"

    # ISBN = sqa.Column(sqa.String)
