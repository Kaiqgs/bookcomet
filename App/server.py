from App import DATABASE_NAME, SYS_LOGIN, SYS_PWD, authorized
from App.Domain import Base
from App.Controllers.db import engine
from App.Controllers.create import router as crouter
from App.Controllers.read import router as rrouter
from App.Controllers.update import router as urouter
from App.Controllers.delete import router as drouter

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from sqlalchemy_schemadisplay import create_schema_graph


app = FastAPI(
    title="BookCometStorage",
    description="",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/")
async def home():
    return {"about": "Welcome to BookComet storage interface."}


class AuthIn(BaseModel):
    login: str
    password: str


@app.post("/signin", status_code=200)
async def signin(authentication: AuthIn):
    global authorized

    if authentication.login == SYS_LOGIN and \
            authentication.password == SYS_PWD:
        authorized = True
        return {"detail": "Sucess signing in."}
    else:
        raise HTTPException(401, "Wrong credentials.")


@app.post("/signoff", status_code=200)
async def signoff():
    global authorized
    if authorized:
        authorized = False
        return {}
    raise HTTPException(422, "You're already signed off.")

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
else:  # Otherwise join an existing one;
    print(f"Available databases: {existing_databases}")
    engine.execute(f"USE {DATABASE_NAME};")

graph = create_schema_graph(metadata=Base.metadata,
                            show_datatypes=True,
                            show_indexes=True,
                            concentrate=False)

# graph.set_size('"5,5!"')
graph.set_dpi('"300"')
graph.write_png('schema.png')

app.include_router(crouter)  # C
app.include_router(urouter)  # R
app.include_router(rrouter)  # U
app.include_router(drouter)  # D, routers
