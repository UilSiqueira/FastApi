from decouple import config

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker


TEST_MODE = config("TEST_MODE", default=False, cast=bool)
DB_URL = config("DB_URL_TEST") if TEST_MODE else config("DB_URL")

engine: AsyncEngine = create_async_engine(
    DB_URL, pool_size=20,
    max_overflow=10,
    pool_timeout=30, 
    pool_pre_ping=True
)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)
