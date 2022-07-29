"""Domain model

About domain model:
- you can replace one implementation with another at a later time.
- you can unit test your controller when needed.
"""


from sqlalchemy.orm import declarative_base

Base = declarative_base()
