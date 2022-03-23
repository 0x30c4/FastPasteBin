from db.models import Bindata
from main import app
# from configs.config import description

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is to include backend dir in sys.path so that we can import
# from db,main.py

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


TestingSessionLocal = sessionmaker(
                                autocommit=False, autoflush=False, bind=engine
                                )

APP_URL = os.environ["APP_URL"]
APP_URL_UPLOAD = os.environ["APP_URL_UPLOAD"]

Bindata.metadata.create_all(bind=engine)


client = TestClient(app)


# def test_index_redirect():
#     response = client.get("/")

#     assert response.url == 1
#     # assert response.status_code == 301


def test_create_paste_json_response():

    params = {
        'meta_data': 'test',
        'rf': 'json',
    }

    files = {
        'file': ('main.py', open('main.py', 'rb')),
    }

    response = client.post(
        "/", params=params, files=files
    )

    assert response.status_code == 201
    data = response.json()

    assert "uuid" in data
    assert data["is_tmp"] is False
    assert data["meta_data"] == "test"
    assert data["url"] == os.path.join(APP_URL, APP_URL_UPLOAD, data["uuid"])

    # TODO: add test to get the paste from the url


def test_create_paste_url_response():
    params = {
        'meta_data': 'test',
        'rf': 'url',
    }

    files = {
        'file': ('main.py', open('main.py', 'rb')),
    }

    response = client.post(
        "/", params=params, files=files
    )

    assert response.status_code == 201

    data = response.text

    assert os.path.join(APP_URL, APP_URL_UPLOAD) in data

    # TODO: add test to get the paste from the url
