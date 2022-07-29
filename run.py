"""Run the App

Ask uvicorn to reference this imported app.

: uvicorn run:app
"""
from sqlalchemy_schemadisplay import create_schema_graph

from App.Domain import Base
from App.server import app, connect_get_database

connect_get_database()

# Creating DB schema visualization;
graph = create_schema_graph(metadata=Base.metadata,
                            show_datatypes=True,
                            show_indexes=True,
                            concentrate=False)
#pylint: disable=no-member
graph.set_dpi('"300"')
graph.write_png('schema.png')
#pylint: enable=no-member
