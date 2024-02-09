from app.db.base import Base
from app.db.connection import engine


async def create_tables() -> None:
    import app.db.__all__models

    print("Creating the database tables")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables was created successfuly")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
