import sqlalchemy as sqa
from sqlalchemy.orm import relationship

# Specific to mysql: MySQL compliant;
from sqlalchemy.dialects.mysql import INTEGER
from App.Domain import Base



class Inventory(Base):
    __tablename__ = "inventory"  # : inventories?

    id = sqa.Column(sqa.String(256), primary_key=True)
    book_id = sqa.Column(sqa.Integer,
                         sqa.ForeignKey("books.id"),
                         primary_key=True)

    quantity = sqa.Column(INTEGER(unsigned=True), nullable=False, default=0)

    book = relationship("Book", back_populates="inventories")

    def __repr__(self) -> str:
        return f"<Inventory: {self.id} w/ {self.quantity:03d}x samples>"
