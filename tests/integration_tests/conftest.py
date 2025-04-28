import pytest_asyncio

from app.backend.db import async_session_maker
from app.auth.model import User

from app.queries.user import AsyncUserQueries
from app.auth.schema import CreateUser


@pytest_asyncio.fixture(loop_scope='function')
async def users():
    users: list = [
        CreateUser(username='testtest', email='testtest@mail.run', raw_password='213213werQ'),
        CreateUser(username='testtest1', email='testtest1@mail.run', raw_password='213213werQ'),
        CreateUser(username='testtest2', email='testtest2@mail.run', raw_password='213213werQ'),
    ]
    res = await AsyncUserQueries.create_users(users)
    return res


@pytest_asyncio.fixture(loop_scope='function')
async def delete_users(users: list[User]):
    async with async_session_maker() as conn:
        try:
            for user in users:
                await conn.delete(user)
            await conn.commit()
        except:
            pass

# mock_session = AsyncMock()
#
# async def get_db_override():
#     async with mock_session as conn:
#         yield conn
#
# app.dependency_overrides[get_db] = get_db_override
#
# @pytest_asyncio.fixture
# def mock_db_session():
#     return mock_session


