import pytest
import pytest_asyncio

from app.backend.db import async_session_maker
from app.models.user import User

from app.queries.user import AsyncUserQueries
from app.schemas.user import CreateUser


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
