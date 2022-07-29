from fastapi import FastAPI

from App import DATABASE_NAME
from App.Controllers.create import router as crouter
from App.Controllers.db import engine
from App.Controllers.delete import router as drouter
from App.Controllers.internal import router as irouter
from App.Controllers.read import router as rrouter
from App.Controllers.update import router as urouter
from App.Domain import Base


def connect_get_database():
    """
    Connect App.server.app into MySQL w/ sqlalchemy;
    """
    global engine

    # Connect and detect existing DBs;
    conn = engine.connect()
    existing_databases = conn.execute("SHOW DATABASES;")
    existing_databases = [d[0] for d in existing_databases]

    # Create database if it doesn't exists;
    if DATABASE_NAME not in existing_databases:
        conn.execute(f"CREATE DATABASE {DATABASE_NAME};")
        engine.execute(f"USE {DATABASE_NAME};")
        Base.metadata.create_all(engine)
        print("Created database.")

    # Otherwise join an existing one;
    else:
        engine.execute(f"USE {DATABASE_NAME};")

    return engine


connect_get_database()
description = \
"""
BookComet storage for inventory manegemnt 🚀.


## Book
You can:
* **Create books**;
* **Read books**;
* **Update books**;
* **Delete books**;

Every book needs an author.
So make sure to input the author in first.

## Author

The author is the creator of an book.
Pass the author name as input when creating a book.

## eBook
Just like a book, but with digital attributes.

## Inventory
Store and manage books.
"""

app = FastAPI(
    title="BookCometStorage",
    description=description,
    version="0.0.A",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Kaique dos Santos",
        "url": "https://github.com/Kaiqgs",
        "email": "kags_@live.com",
    },
    license_info={
        "name": "GNU 3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0-standalone.html",
    },
)

app.include_router(irouter)
app.include_router(crouter)  # C;
app.include_router(urouter)  # R;
app.include_router(rrouter)  # U;
app.include_router(drouter)  # D, routers;
