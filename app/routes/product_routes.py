from typing import List
from fastapi import APIRouter, Response, Depends, status
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.use_cases.product import ProductUseCases
from app.schemas.product import Product, ProductOutput
from app.schemas.product import ProductInput


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


@router.get("/list", response_model=List[ProductOutput], description="List products")
async def list_products(search: str = "", db_session: Session = Depends(get_db_session)):
    uc = ProductUseCases(db_session=db_session)
    products = await uc.list_products(search=search)

    return products