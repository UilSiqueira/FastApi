from typing import List
from fastapi import APIRouter, Response, Depends, status, Query
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.use_cases.product import ProductUseCases
from app.schemas.product import Product, ProductOutput
from app.schemas.product import ProductInput
from fastapi_pagination import Page


router = APIRouter(prefix="/product", tags=["Product"])


@router.post("/add", status_code=status.HTTP_201_CREATED, description="Add new product")
async def add_product(product_input: ProductInput, db_session: Session = Depends(get_db_session)):

    uc = ProductUseCases(db_session=db_session)
    await uc.add_product(
        product=product_input.product, category_slug=product_input.category_slug
    )

    return Response(status_code=status.HTTP_201_CREATED)


@router.put("/update/{id}", description="Update product")
async def update_product(id: int, product: Product, db_session: Session = Depends(get_db_session)):

    uc = ProductUseCases(db_session=db_session)
    await uc.update_product(id=id, product=product)

    return Response(status_code=status.HTTP_200_OK)


@router.delete("/delete/{id}", description="Delete product")
async def delete_product(id: int, db_session: Session = Depends(get_db_session)):

    uc = ProductUseCases(db_session=db_session)
    await uc.delete_product(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.get("/list", response_model=Page[ProductOutput], description="List products")
async def list_products(
    page: int = Query(1, ge=1, description='Page number'),
    size: int = Query(50, ge=1, le=100, description='Page size'),
    search: str = "",
    db_session: Session = Depends(get_db_session)
): 
    uc = ProductUseCases(db_session=db_session)
    products = await uc.list_products(page=page, size=size, search=search)

    return products
