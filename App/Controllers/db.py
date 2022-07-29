from sqlalchemy import create_engine

# Redundant import, to ensure DataBase.metadata collection;
import App.Domain.author
import App.Domain.book
import App.Domain.ebook
import App.Domain.inventory
import App.Domain.publication
from App import DB_PATH

engine = create_engine(DB_PATH, connect_args=dict(host='localhost', port=3306))
