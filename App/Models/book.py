# Since implementation of books and e-books is tricky w/ sql**, Interface pattern was picked;
# # ** due to no auto mapping for parent relationship attributes, w/ foreign key inheritance;
# Book Interface;
class IBook:
    __abstract__ = True
    id: int
    name: str
    authors: list
    publisher: str
    yearofpub: int
    summary: str
