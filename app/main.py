import asyncio

from watchfiles import awatch

from app.quaries.core import AsyncCoreQueries
from app.quaries.orm import AsyncOrmQueries

async def main_():
    await AsyncCoreQueries.create_tables()
    await AsyncOrmQueries.insert_data()
    await AsyncCoreQueries.select_data()
    await AsyncCoreQueries.insert_data()
    await AsyncCoreQueries.update_data()
    await AsyncOrmQueries.select_data()
    await AsyncOrmQueries.update_data()
    await AsyncOrmQueries.load_resumes()

asyncio.run(main_())
