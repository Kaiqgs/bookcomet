import http.client as code

from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from App import SYS_LOGIN, SYS_PWD, simple_session
from App.Controllers import Routes

router = APIRouter()


@router.get(Routes.Home.value)
async def home():
    "First user interaction."
    return {"about": "Welcome to BookComet storage interface."}


class AuthIn(BaseModel):
    "Authorization input."
    login: str
    password: str


@router.post(Routes.SignIn.value, status_code=code.OK.value)
async def signin(authentication: AuthIn):
    "Signs in based on authentication input."
    if authentication.login == SYS_LOGIN and \
            authentication.password == SYS_PWD:
        simple_session["authorized"] = True
        return {"detail": "Sucess signing in."}
    else:
        raise HTTPException(code.UNAUTHORIZED.value, "Wrong credentials.")


@router.post(Routes.SignOff.value, status_code=code.OK.value)
async def signoff():
    "Signs off, therefore removing authorization."
    if simple_session["authorized"]:
        simple_session["authorized"] = False
        return {"detail": "Sucess signing off."}
    raise HTTPException(
        code.UNPROCESSABLE_ENTITY.value,
        "You're already signed off.")


@router.post(Routes.SetTesting.value, status_code=code.OK.value)
async def set_testing(state: bool):
    "Sets the state of development-testing functionality."

    simple_session["testing"] = state
    return {"detail": "Sucess setting developing debug mode."}
