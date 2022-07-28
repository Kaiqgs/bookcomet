from sqlalchemy import create_engine

import App.Domain.book
import App.Domain.author
import App.Domain.publication
import App.Domain.ebook
import App.Domain.inventory
from App import DB_PATH


engine = create_engine(DB_PATH, connect_args=dict(host='localhost', port=3306))