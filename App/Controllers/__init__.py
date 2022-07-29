from enum import Enum

# Regex for matching unvalued Routes:
# (Routes\.)(\w*)[,:;\s\n\r!?\\-\]\[\)\(]


class Routes(Enum):
    """
    Enumerates operations and URIs.
    """
    CreateAuthor = "/new-author/"
    CreateBook = "/new-book/{author}"
    CreateEBook = "/new-ebook/"
    CreateInventory = "/new-inventory/"
    NewSamples = "/new-samples/{quantity}"

    ReadBooks = "/list-books/"

    DeleteBook = "/delete-book/{id}"

    UpdateBook = "/update-book/{id}"

    SetTesting = "/set-testing/{state}"
    SignIn = "/signin/"
    SignOff = "/signoff/"
    Home = "/"
