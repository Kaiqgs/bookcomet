import sqlalchemy as sqa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from App.Domain import Base
from App.Models.book import IBook
from App.Models.ebook import Formats


class eBook(Base, IBook):
    """
    eBook, Book inheritance via property override;
    """
    __tablename__ = "ebooks"

    id = sqa.Column(sqa.Integer,
                    sqa.ForeignKey("books.id"),
                    primary_key=True)

    format = sqa.Column(sqa.Enum(Formats), nullable=False)

    book: IBook = relationship("Book", back_populates="digital")

    @hybrid_property
    def name(self):
        return self.book.name

    @hybrid_property
    def authors(self):
        return self.book.authors

    @hybrid_property
    def publisher(self):
        return self.book.publisher

    @hybrid_property
    def yearofpub(self):
        return self.book.yearofpub

    @hybrid_property
    def summary(self):
        return self.book.summary

    def __repr__(self) -> str:
        return f"<eBook[{self.id:03d}]: digital {self.format}, {self.name}>"
