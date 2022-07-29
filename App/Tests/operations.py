import http.client as code
import random
import unittest

from fastapi.testclient import TestClient

from App import SYS_LOGIN, SYS_PWD
from App.Controllers import Routes
from App.Controllers.create import BookIn
from App.Controllers.internal import AuthIn
from App.Controllers.update import UpdateBookIn
from App.server import app, connect_get_database
from App.Tests.util import randname, tojson


class TestOperations(unittest.TestCase):
    """
    Operations TestsCases.
    Intended to represent user usage and behaviour.
    """

    def sysignin(self):
        "Signs in with correct login and password."
        response = self.tclient.post(Routes.SignIn.value, tojson(
            AuthIn(login=SYS_LOGIN, password=SYS_PWD)))
        self.assertEqual(response.status_code, code.OK.value)
        return response

    @classmethod
    def setUpClass(cls):
        cls.resources = {}

        cls.tclient = TestClient(app)

        testresp = cls.tclient.post(
            Routes.SetTesting.value.format(state="false"))

        assert testresp.status_code == code.OK.value, "Could not set testing."

        cls.tclient.post(Routes.SignOff.value)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.resources = None
        cls.tclient = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        connect_get_database()

    def test_authorization_flow(self) -> None:
        # logoff while being logged off;
        response = self.tclient.post(Routes.SignOff.value)
        self.assertEqual(response.status_code, code.UNPROCESSABLE_ENTITY.value)

        # attempt wrong credentials;
        response = self.tclient.post(Routes.SignIn.value, tojson(
            AuthIn(login="!@nonexisting!@", password="inexistent")))
        self.assertEqual(response.status_code, code.UNAUTHORIZED.value)

        # attempt reading from wrong credentials;
        response = self.tclient.get(Routes.ReadBooks.value)
        self.assertEqual(response.status_code, code.UNAUTHORIZED.value)

        # login with correct credentials;
        self.sysignin()

        # attempt read with right credentials;
        response = self.tclient.get(Routes.ReadBooks.value)
        self.assertEqual(response.status_code, code.OK.value)

        # attempt logoff;
        response = self.tclient.post(Routes.SignOff.value)
        self.assertEqual(response.status_code, code.OK.value)

    def test_book_creation_flow(self):

        self.sysignin()

        readbookresponse = self.tclient.get(Routes.ReadBooks.value)
        readbookdata = readbookresponse.json()
        self.assertEqual(readbookresponse.status_code, code.OK.value)

        if not readbookdata:
            self.tclient.get(Routes.NewSamples.value.format(1))
            readbookresponse = self.tclient.get(Routes.ReadBooks.value)
            readbookdata = readbookresponse.json()
            self.assertEqual(readbookresponse.status_code, code.OK.value)

        authorname = readbookdata[0]["authors"][0]["name"]
        bookresponse = self.tclient.post(
            Routes.CreateBook.value.format(
                author=authorname), tojson(
                BookIn(
                    name=randname(5), publisher=randname(10), yearofpub=random.randint(
                        1800, 2000), summary=randname(32))))

        bookdata = bookresponse.json()
        self.assertEqual(bookresponse.status_code, code.CREATED.value)

        upresponse = self.tclient.put(
            Routes.UpdateBook.value.format(
                id=bookdata["id"]),
            tojson(
                UpdateBookIn(
                    name=f"new {randname()}",
                    publisher=randname(10),
                    yearofpub=random.randint(
                        1800,
                        2000),
                    summary=f"new {randname(30)}")))

        self.assertEqual(upresponse.status_code, code.OK.value)

        deleteresponse = self.tclient.delete(
            Routes.DeleteBook.value.format(id=bookdata["id"]))

        self.assertEqual(deleteresponse.status_code, code.OK.value)
