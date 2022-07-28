from functools import wraps
from fastapi import HTTPException


DATABASE_NAME = "bookcomet"
DB_PATH = "mysql://root:Kaique123@localhost"
SYS_LOGIN, SYS_PWD = "BookComet", "PureSpec"
authorized = False
testing = True


def sys_authorize(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if authorized or testing:
            return await func(*args, **kwargs)
        else:
            raise HTTPException(401, "Forbidden action, login first.")
    return wrapper
