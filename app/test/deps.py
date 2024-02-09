from decouple import config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from typing import AsyncGenerator
from passlib.context import CryptContext

from app.db.models import Category as CategoryModel
from app.db.models import Product as ProductModel
from app.db.models import User as UserModel
from app.db.connection import Session as asyncSession

crypt_context = CryptContext(schemes=["sha256_crypt"])


async def db_session() -> AsyncGenerator:
    try:
        session: AsyncSession = asyncSession()
        yield session
    finally:
        await session.close()


async def categories_on_db(db_session=db_session()):

    categories = [
        CategoryModel(name="Clothes", slug="clothes"),
        CategoryModel(name="Glasses", slug="glasses"),
    ]

    for category in categories:
        db_session.add(category)
    await db_session.commit()

    for category in categories:
        await db_session.refresh(category)
    return categories


async def delete_categories_on_db(db_session):
    categories = await db_session.execute(select(CategoryModel))
    for category in categories.scalars().unique().all():
        await db_session.delete(category)
    await db_session.commit()


async def product_on_db(db_session):
    category = CategoryModel(name="Clothes", slug="clothes")
    db_session.add(category)
    await db_session.commit()

    product = ProductModel(
        name="T-shirt", slug="t-shirt", price=100.99, stock=20, category_id=category.id
    )

    db_session.add(product)
    await db_session.commit()
    return product


async def delete_products_on_db(db_session):
    products = await db_session.execute(select(ProductModel))
    for product in products.scalars().unique().all():
        await db_session.delete(product)
    await db_session.commit()

    # delete foreign key
    await delete_categories_on_db(db_session)


async def user_on_db(db_session):
    user = UserModel(username="JohnDoe", password=crypt_context.hash("pass#"))

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


async def delete_user_on_db(db_session, user_on_db):
    await db_session.delete(user_on_db)
    await db_session.commit()


async def clear_test_db(new_session=db_session):
    TEST_MODE = config("TEST_MODE", default=False, cast=bool)
    if TEST_MODE is True:
        async for session in new_session():
            await session.execute(delete(UserModel).where(True))
            await session.execute(delete(ProductModel).where(True))
            await session.execute(delete(CategoryModel).where(True))
            await session.commit()
