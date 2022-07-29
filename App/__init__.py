from functools import wraps

from fastapi import HTTPException

DATABASE_NAME = "bookcomet"
DB_PATH = "mysql://root:Kaique123@localhost"
SYS_LOGIN, SYS_PWD = "BookComet", "PureSpec"

simple_session = {
    "testing": True,
    "authorized": False
}


def sys_authorize(func):
    """
    Simple session authorization decorator.
    Used to wrap authentication functionality into routable functions;
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if simple_session["authorized"] or simple_session["testing"]:
            return await func(*args, **kwargs)
        else:
            raise HTTPException(401, "Forbidden action, login first.")
    return wrapper
