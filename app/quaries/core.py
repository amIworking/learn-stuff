from typing import Annotated

from fastapi import Depends
from sqlalchemy import text, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_engine, async_session_maker, Base
from app.models import Worker


# from app.models import metadata_obj, workers_table


async def get_db() -> AsyncSession:
    async with async_session_maker() as ac:
        yield ac



async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_version():
    async with async_engine.connect() as ac:
        res = await ac.execute(text('SELECT VERSION()'))
        print(f'{res.first()=}')
        # yield res


async def insert_data():
    new_worker: Worker = Worker(username='test6')
    async with async_session_maker() as ac:
        ac.add(new_worker)
        await ac.commit()