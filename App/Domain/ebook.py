from App.Models.book import IBook
from App.Models.ebook import Formats

from App.Domain import Base

import sqlalchemy as sqa
from sqlalchemy.orm import relationship


class eBook(Base, IBook):
    __tablename__ = "ebooks"

    id = sqa.Column(sqa.Integer,
                    sqa.ForeignKey("books.id"),
                    primary_key=True)

    format = sqa.Column(sqa.Enum(Formats), nullable=False)

    book = relationship("Book", back_populates="digital")

    def __repr__(self) -> str:
        return f"<eBook[{self.id:03d}]: {self.format}>"
