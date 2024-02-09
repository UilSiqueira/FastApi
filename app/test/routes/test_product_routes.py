from fastapi import status
from app.main import app
import httpx
from app.test.deps import (
    db_session,
    categories_on_db,
    delete_products_on_db,
    product_on_db,
)

# constants
HTTP_201_CREATED = status.HTTP_201_CREATED
HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND
HTTP_200_OK = status.HTTP_200_OK

BASE_URL = "http://testserver"

headers = {"Authorization": "Bearer token"}


async def test_add_product_route(db_session=db_session):
    async for session in db_session():
        categories = await categories_on_db(session)
        category_slug = categories[0].slug

        body = {
            "category_slug": category_slug,
            "product": {
                "name": "Camisa Mike",
                "slug": "camisa-mike",
                "price": 23.99,
                "stock": 23,
            },
        }

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.post("/product/add", json=body, headers=headers)
        await delete_products_on_db(session)

    assert (response.status_code == HTTP_201_CREATED), \
        f"Result: {response.status_code}, Expected: {HTTP_201_CREATED}"


async def test_add_product_route_invalid_category_slug():

    body = {
        "category_slug": "invalid",
        "product": {
            "name": "Camisa Mike",
            "slug": "camisa-mike",
            "price": 23.99,
            "stock": 23,
        },
    }

    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/product/add", json=body)

    assert (response.status_code == HTTP_404_NOT_FOUND), \
        f"Result: {response.status_code}, Expected: {HTTP_404_NOT_FOUND}"


async def test_update_product_route(db_session=db_session):
    async for session in db_session():
        product = await product_on_db(session)

        body = {
            "name": "Updated T-shirt",
            "slug": "updated-t-shirt",
            "price": 23.88,
            "stock": 10,
        }

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.put(f"/product/update/{product.id}", json=body)
        await delete_products_on_db(session)

    assert (response.status_code == HTTP_200_OK), \
        f"Result: {response.status_code}, Expected: {HTTP_200_OK}"


async def test_update_product_route_invalid_id():

    body = {
        "name": "Updated camisa",
        "slug": "updated-camisa",
        "price": 23.88,
        "stock": 10,
    }

    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.put("/product/update/1", json=body)

    assert (response.status_code) == HTTP_404_NOT_FOUND, \
        f"Result: {response.status_code}, Expected: {HTTP_404_NOT_FOUND}"


async def test_delete_product_route(db_session=db_session):
    async for session in db_session():
        product = await product_on_db(session)

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.delete(f"/product/delete/{product.id}")
        await delete_products_on_db(session)

    assert (response.status_code == HTTP_200_OK), \
        f"Result: {response.status_code}, Expected: {HTTP_200_OK}"


async def test_delete_product_route_invalid_id():
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.delete("/product/delete/1")

    assert (response.status_code == HTTP_404_NOT_FOUND), \
        f"Result: {response.status_code}, Expected: {HTTP_404_NOT_FOUND}"


async def test_list_products_route(db_session=db_session):
    async for session in db_session():
        product = await product_on_db(session)

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.get("/product/list")

        data = response.json()
        product_slug = product.slug

        await delete_products_on_db(session)

    assert (data[0]["slug"] == product_slug), \
        f"Result: {data[0]['slug']}, Expected: {product_slug}"
    assert (response.status_code == HTTP_200_OK), \
        f"Result: {response.status_code}, Expected: {HTTP_200_OK}"


async def test_list_products_route_with_search(db_session=db_session):

    async for session in db_session():
        products_on_db = await product_on_db(session)

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.get("/product/list?search=t-shirt")

        data = response.json()
        product_slug = products_on_db.slug

        await delete_products_on_db(session)

    assert (response.status_code == HTTP_200_OK), \
        f"Result: {response.status_code},  Expected: {HTTP_200_OK}"
    assert len(data) == 1
    assert (data[0]["slug"] == product_slug), \
        f"Result: {data[0]['slug']}, Expected: {product_slug}"
