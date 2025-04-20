from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# sync_engine = create_engine(
#     url=settings.DATABASE_URL_sync,
#     echo=True
# )
#
# with sync_engine.connect() as conn:
#     res = conn.execute(text('SELECT VERSION()'))
#     print(f'{res=}')
#
async_engine = create_async_engine(
    url=settings.DATABASE_URL_async,
    echo=True
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass