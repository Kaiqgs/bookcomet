"""Controllers

Handling of requests and data management.
"""

from enum import Enum

# Regex for matching unvalued Routes:
# (Routes\.)(\w*)[,:;\s\n\r!?\\-\]\[\)\(]


class Routes(Enum):
    """
    Enumerates operations and URIs.
    """

    CREATE_AUTHOR = "/new-author/"
    CREATE_BOOK = "/new-book/{author}"
    CREATE_EBOOK = "/new-ebook/"
    CREATE_INVENTORY = "/new-inventory/"
    CREATE_SAMPLES = "/new-samples/{quantity}"

    READ_BOOKS = "/list-books/"

    DELETE_BOOK = "/delete-book/{id}"

    UPDATE_BOOK = "/update-book/{id}"

    SET_TESTING = "/set-testing/{state}"
    SIGNIN = "/signin/"
    SIGNOFF = "/signoff/"
    HOME = "/"
