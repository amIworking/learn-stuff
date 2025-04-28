import pytest
from contextlib import nullcontext as does_not_raise
from fastapi import status
from httpx import AsyncClient, ASGITransport, Client

from app.main import app
from app.auth.model import User

API_URL: str = 'http://127.0.0.1:8888/api/v1'
USER_API_URL: str = API_URL + '/users'

# async def get_async_client() -> AsyncClient:
#     async with AsyncClient(
#             transport=ASGITransport(app=app), base_url=USER_API_URL
#     ) as ac:
#         yield ac

class TestUser:
    @pytest.mark.parametrize(
        'username, email, password, expectation',
        [
            ('boben', 'boben@gmail.com', 'Qwerty12', does_not_raise()),
            # ('robin', 'robin@gmail.com', 'Qwerty12', does_not_raise()),
            ('steve', 'ail.com', 'Qwerty12', pytest.raises(AssertionError)), # Because of a wrong email,
            ('steve', 'gmail.com', 'Qwerty12', pytest.raises(AssertionError)),  # Because of a wrong email,
            ('steve', 'f.com', 'Qwerty12', pytest.raises(AssertionError)),  # Because of a wrong email
            ('e', 'e@gmail.com', 'Qwerty12', pytest.raises(AssertionError)), # Because of a short username
            ('edf'*11, 'steve@gmail.com', 'Qwerty12', pytest.raises(AssertionError)), # Because of a long username
            ('alice', 'alice@gmail.com', 'qwerty', pytest.raises(AssertionError)), # Because of a short password
        ]
    )
    @pytest.mark.asyncio
    async def test_create_user(self, username, email, password, expectation):
        with expectation:
            new_user: dict = {
                'username': username,
                'email': email,
                'raw_password': password
            }
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url=USER_API_URL
            ) as ac:
                response = await ac.post('/', json=new_user)
                await ac.aclose()

            assert response.status_code == status.HTTP_201_CREATED
            user_data: dict = response.json()
            assert user_data['email'] == email
            assert user_data['username'] == username


    @pytest.mark.asyncio
    async def test_show_user(self, users: list[User]):
        user: User = users[0]
        async with AsyncClient(
                transport=ASGITransport(app=app), base_url=USER_API_URL
        ) as ac:
            response_by_id = await ac.get(url=f'/{user.id}/')
            response_by_username = await ac.get(url=f'/{user.username}/')


        assert response_by_id.status_code == status.HTTP_200_OK
        assert response_by_username.status_code == status.HTTP_200_OK

        user_data: dict = response_by_id.json()
        assert user_data == response_by_username.json()

        assert user_data['username'] == user.username
        assert user_data['email'] == user.email


    @pytest.mark.asyncio
    async def test_update_user(self):
        pass


    @pytest.mark.asyncio
    async def test_delete_user(self):
        pass
