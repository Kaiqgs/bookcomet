import sqlalchemy as sqa

from App.Domain import Base


class Publication(Base):
    """
    Publication ORM association table.
    Used to link Author <-> Books.
    """
    # Wondering: should publisher be stored in publication?

    __tablename__ = 'publications'
    authorid = sqa.Column("author_id",
                          sqa.Integer,
                          sqa.ForeignKey('authors.id'),
                          primary_key=True,
                          nullable=False)

    bookid = sqa.Column("book_id",
                        sqa.Integer,
                        sqa.ForeignKey('books.id'),
                        primary_key=True,
                        nullable=False)

    def __repr__(self) -> str:
        return f"<Publication: #{self.authorid:03d} #{self.bookid:03d}>"

    #author = relationship("Author", back_populates="releases")
    #book = relationship("Book", back_populates ="authors")
