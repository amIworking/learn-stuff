import asyncio
from app.queries.user import AsyncUserQueries
from watchfiles import awatch

from app.queries.core import AsyncCoreQueries
from app.schemas.user import CreateUser


# from app.queries.core import AsyncCoreQueries
# from app.queries.orm import AsyncOrmQueries
#
# async def main_():

#     await AsyncOrmQueries.insert_data()
#     await AsyncCoreQueries.select_data()
#     await AsyncCoreQueries.insert_data()
#     await AsyncCoreQueries.update_data()
#     await AsyncOrmQueries.select_data()
#     await AsyncOrmQueries.update_data()
#     await AsyncOrmQueries.load_resumes()
#     await AsyncOrmQueries.select_resumes_avg_comp()



async def main_():
    await AsyncUserQueries.load_data()
    user_data = {
        'email': 'test@mail.ru',
        'username': 'test',
        'raw_password': 'Wrerew123456'
    }
    await AsyncUserQueries.create_user(user_data=CreateUser(**user_data))
    await AsyncUserQueries.show_user(id_or_username='20984256-0eb0-4cba-8da3-9830cd30154c')
    await AsyncUserQueries.show_user(id_or_username='some_user2')

asyncio.run(main_())
