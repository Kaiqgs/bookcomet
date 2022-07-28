from App.server import app
from fastapi.testclient import TestClient


tclient = TestClient(app)
