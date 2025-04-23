from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.backend.config import settings

test_sync_engine = create_engine(
    url=settings.TEST_DATABASE_URL_sync,
    echo=True
)


test_async_engine = create_async_engine(
    url=settings.TEST_DATABASE_URL_async,
    echo=True
)

test_async_session_maker = async_sessionmaker(
    bind=test_async_engine,
    expire_on_commit=False,
)
