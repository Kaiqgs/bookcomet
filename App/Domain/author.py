import sqlalchemy as sqa
from sqlalchemy.orm import relationship

from App.Domain import Base
from App.Domain.publication import Publication


class Author(Base):
    """
    Author entity ORM mapped.
    """
    __tablename__ = "authors"

    id = sqa.Column(sqa.Integer, primary_key=True)
    name = sqa.Column(sqa.String(256), nullable=False, unique=True)
    releases = relationship("Book",
                            secondary=Publication.__table__,
                            back_populates="authors",
                            cascade="all, delete")

    def __repr__(self) -> str:
        return f"<Author[{self.id:03d}]: {self.name}>"
