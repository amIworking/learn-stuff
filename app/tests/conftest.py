from email.policy import default

import pytest
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.backend.config import settings
from app.backend.db import sync_engine, Base


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    assert settings.MODE == 'TEST'
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)

def pytest_addoption(parser):
    parser.addoption(
        "--drop_db",
        default='false',
        choices=('false', 'true')
    )

@pytest.fixture(scope='session')
def does_drop_db(request):
    return request.config.getoption('--drop_db')


@pytest.fixture(scope='session', autouse=True)
def drop_db(does_drop_db):
    yield
    if does_drop_db == 'true':
        assert settings.MODE == 'TEST'
        if database_exists(sync_engine.url):
            drop_database(sync_engine.url)