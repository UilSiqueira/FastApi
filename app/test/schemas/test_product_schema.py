import pytest
from app.schemas.product import Product, CategoryOutput, ProductInput, ProductOutput


async def test_product_schema():
    product = Product(name="T-shirt", slug="t-shirt", price=22.99, stock=22)

    assert product.model_dump() == {
        "name": "T-shirt",
        "slug": "t-shirt",
        "price": 22.99,
        "stock": 22,
    }


async def test_product_schema_invalid_slug():
    with pytest.raises(ValueError):
        Product(name="T-shirt", slug="t shirt", price=22.99, stock=22)


async def test_product_schema_invalid_price():
    with pytest.raises(ValueError):
        Product(name="Camisa Mike", slug="camisa-mike", price=0, stock=22)


async def test_product_input_schema():
    product = Product(name="Camisa Mike", slug="camisa-mike", price=22.99, stock=22)

    product_input = ProductInput(category_slug="roupa", product=product)

    assert product_input.model_dump() == {
        "category_slug": "roupa",
        "product": {
            "name": "Camisa Mike",
            "slug": "camisa-mike",
            "price": 22.99,
            "stock": 22,
        },
    }


async def test_product_output_schema():
    category = CategoryOutput(id=1, name="Roupa", slug="roupa")

    product_output = ProductOutput(
        id=1, name="Camisa", slug="camisa", price=10, stock=10, category=category
    )

    assert product_output.model_dump() == {
        "id": 1,
        "name": "Camisa",
        "slug": "camisa",
        "price": 10,
        "stock": 10,
        "category": {"id": 1, "name": "Roupa", "slug": "roupa"},
    }
