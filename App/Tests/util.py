
import json
import random
import string

from fastapi.encoders import jsonable_encoder


def tojson(obj):
    "FastAPI converter from object to json."
    return json.dumps(jsonable_encoder(obj))


def randname(amt=10):
    "Returns random string of size N."
    return "".join(random.choice(string.ascii_letters + " ")
                   for _ in range(amt))
