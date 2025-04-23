
import pytest
from contextlib import nullcontext as does_not_raise

from email_validator import EmailSyntaxError
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy_utils import database_exists, create_database

from app.backend.db import Base
from app.models.user import User
from app.queries.user import AsyncUserQueries
from app.schemas.user import CreateUser
from app.tests.db_config_for_tests import test_sync_engine, test_async_session_maker


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    if not database_exists(test_sync_engine.url):
        create_database(test_sync_engine.url)
    Base.metadata.drop_all(test_sync_engine)
    Base.metadata.create_all(test_sync_engine)

@pytest.fixture
async def users():
    users: list = [
        CreateUser(username='testtest', email='testtest@mail.run', raw_password='213213werQ'),
        CreateUser(username='testtest1', email='testtest1@mail.run', raw_password='213213werQ'),
        CreateUser(username='testtest2', email='testtest2@mail.run', raw_password='213213werQ'),
    ]
    res = await AsyncUserQueries.create_users(users, session_maker=test_async_session_maker)
    return res

@pytest.fixture
async def delete_users(users: list[User]):
    async with test_async_session_maker() as conn:
        try:
            for user in users:
                await conn.delete(user)
            await conn.commit()
        except:
            pass


class TestUser:
    # @pytest.mark.parametrize(
    #     'username, email, password, expectation',
    #     [
    #         ('boben', 'boben@gmail.com', 'Qwerty12', does_not_raise()),
    #         ('steve', 'ail.com', 'Qwerty12', pytest.raises(ValidationError)),
    #         ('e', 'e@gmail.com', 'Qwerty12', pytest.raises(ValidationError)),
    #         ('alice', 'alice@gmail.com', 'qwerty', pytest.raises(ValidationError)),
    #     ]
    # )
    # @pytest.mark.asyncio
    # async def test_create_user(self, username, email, password, expectation):
    #     with expectation:
    #         new_user: CreateUser = CreateUser(username=username, email=email, raw_password=password)
    #         user_data = await AsyncUserQueries.create_user(new_user)
    #         assert user_data['username'] == username
    #         assert user_data['email'] == email
    #         print()

    @pytest.mark.asyncio
    async def test_show_user(self, users: list[User]):
        user: User = users[0]
        user_by_id: dict = await AsyncUserQueries.show_user(
            id_or_username=str(user.id),
            session_maker=test_async_session_maker
        )
        user_by_username: dict = await AsyncUserQueries.show_user(
            id_or_username=user.username,
            session_maker=test_async_session_maker
        )
        assert user_by_id == user_by_username
        print()
    #
    # async def test_update_user(self, user_id):
    #     pass
    #
    # async def test_delete_user(self, user_id):
    #     pass