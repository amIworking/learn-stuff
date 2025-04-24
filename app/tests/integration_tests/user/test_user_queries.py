#
# class TestUserQueries:
#     @pytest.mark.parametrize(
#         'username, email, password, expectation',
#         [
#             ('boben', 'boben@gmail.com', 'Qwerty12', does_not_raise()),
#             ('steve', 'ail.com', 'Qwerty12', pytest.raises(ValidationError)),
#             ('e', 'e@gmail.com', 'Qwerty12', pytest.raises(ValidationError)),
#             ('alice', 'alice@gmail.com', 'qwerty', pytest.raises(ValidationError)),
#         ]
#     )
#     @pytest.mark.asyncio
#     async def test_queries_create_user(self, username, email, password, expectation):
#         with expectation:
#             new_user: CreateUser = CreateUser(username=username, email=email, raw_password=password)
#             user_data = await AsyncUserQueries.create_user(new_user)
#             assert user_data['username'] == username
#             assert user_data['email'] == email
#             print()
#
#
#     @pytest.mark.asyncio
#     async def test_queries_show_user(self, users: list[User]):
#         print()
#         #user_list = await users
#         user: User = users[0]
#         print(user)
#         user_by_id: dict = await AsyncUserQueries.show_user(
#             id_or_username=str(user.id)
#         )
#         user_by_username: dict = await AsyncUserQueries.show_user(
#             id_or_username=user.username
#         )
#         assert user_by_id == user_by_username
#         print()



    # async def test_queries_update_user(self, user_id):
    #     pass
    #
    # async def test_queries_delete_user(self, user_id):
    #     pass
