import pytest
from fastapi.exceptions import HTTPException
from app.db.models import Product as ProductModel
from app.schemas.product import Product, ProductOutput
from app.use_cases.product import ProductUseCases

from sqlalchemy.future import select

from app.test.deps import (
    db_session,
    categories_on_db,
    delete_products_on_db,
    product_on_db,
)


async def test_add_product_uc(db_session=db_session):
    async for session in db_session():
        category = await categories_on_db(session)
        category_slug = category[0].slug

        product = Product(name="T-shirt", slug="t-shirt", price=22.99, stock=22)

        uc = ProductUseCases(session)
        await uc.add_product(product=product, category_slug=category_slug)

        query = select(ProductModel)
        result = await session.execute(query)
        product_from_db = result.scalars().unique().all()

        await delete_products_on_db(session)

    assert product_from_db[0].name == product.name, \
        f"Result: {product_from_db[0].name}, Expected: {product.name}"
    assert product_from_db[0].slug == product.slug, \
        f"Result: {product_from_db[0].slug}, Expected: {product.slug}"
    assert product_from_db[0].price == product.price, \
        f"Result: {product_from_db[0].price}, Expected: {product.price}"
    assert product_from_db[0].stock == product.stock, \
        f"Result: {product_from_db[0].stock}, Expected: {product.stock}"


async def test_add_product_uc_invalid_category(db_session=db_session):
    async for session in db_session():
        uc = ProductUseCases(session)

        product = Product(name="T-shirt", slug="t-shirt", price=22.99, stock=22)
        with pytest.raises(HTTPException):
            await uc.add_product(product=product, category_slug="invalid")


async def test_update_product(db_session=db_session):
    async for session in db_session():
        products = await product_on_db(session)

        product = Product(name="T-shirt", slug="t-shirt", price=22.99, stock=22)

        uc = ProductUseCases(session)
        await uc.update_product(id=products.id, product=product)

        query = select(ProductModel).filter(ProductModel.id == products.id)
        result = await session.execute(query)
        product_updated_on_db = result.scalars().unique().one_or_none()

        await delete_products_on_db(session)

    assert (product_updated_on_db is not None), \
        f"Result: {product_updated_on_db is not None}, Expected: Product is True"
    assert (product_updated_on_db.name == product.name), \
        f"Result: {product_updated_on_db.name}, Expected: {product.name}"
    assert (product_updated_on_db.slug == product.slug), \
        f"Result: {product_updated_on_db.slug}, Expected: {product.slug}"
    assert (product_updated_on_db.price == product.price), \
        f"Result: {product_updated_on_db.price}, Expected: {product.price}"
    assert (product_updated_on_db.stock == product.stock), \
        f"Result: {product_updated_on_db.stock}, Expected: {product.stock}"


async def test_update_product_invalid_id(db_session=db_session):
    async for session in db_session():
        product = Product(name="T-shirt", slug="t-shirt", price=22.99, stock=22)

        uc = ProductUseCases(session)

        with pytest.raises(HTTPException):
            await uc.update_product(id=1, product=product)


async def test_delete_product(db_session=db_session):
    async for session in db_session():
        product = await product_on_db(session)

        uc = ProductUseCases(session)
        await uc.delete_product(id=product.id)

        query = select(ProductModel)
        result = await session.execute(query)
        categories_from_db = result.scalars().unique().all()

        assert len(categories_from_db) == 0


async def test_delete_product_non_exist(db_session=db_session):
    async for session in db_session():
        uc = ProductUseCases(session)

        with pytest.raises(HTTPException):
            await uc.delete_product(id=1)


async def test_list_products_uc(db_session=db_session):
    async for session in db_session():
        product_from_db = await product_on_db(session)

        uc = ProductUseCases(session)

        products = await uc.list_products()

        product_from_db_name = product_from_db.name
        category_name = product_from_db.category["name"]
        await delete_products_on_db(session)

    assert len(products) == 1, \
        f"Result: {len(products)}, Expected: {1}"
    assert (type(products[0]) is ProductOutput), \
        f"Result: {type(products[0])}, Expected: {ProductOutput}"
    assert (products[0].name == product_from_db_name), \
        f"Result: {products[0].name}, Expected: {product_from_db_name}"
    assert (products[0].category.name == category_name), \
        f"Result: {products[0].category.name}, Expected: {category_name}"


async def test_list_products_with_search(db_session=db_session):
    async for session in db_session():
        product_from_db = await product_on_db(session)
        uc = ProductUseCases(session)

        products = await uc.list_products(search="t-shirt")

        product_from_db_name = product_from_db.name
        category_name = product_from_db.category["name"]
        await delete_products_on_db(session)

    assert len(products) == 1, \
        f"Result: {len(products)}, Expected: {1}"
    assert (type(products[0]) is ProductOutput), \
        f"Result: {type(products[0])}, Expected: {ProductOutput}"
    assert (products[0].name == product_from_db_name), \
        f"Result: {products[0].name}, Expected: {product_from_db_name}"
    assert (products[0].category.name == category_name), \
        f"Result: {products[0].category.name}, Expected: {category_name}"
