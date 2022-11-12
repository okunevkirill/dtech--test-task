__all__ = [
    "router",
]

from fastapi import APIRouter, status

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/",
            status_code=status.HTTP_200_OK,
            summary="List of all products")
async def get_all_products():
    return "Place for advertising"


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             summary="Add new product")
async def add_product():
    return "Place for advertising"


@router.put("/{product_id}",
            status_code=status.HTTP_200_OK,
            summary="Update product")
async def update_product(product_id: int):
    return f"Update {product_id} product"


@router.delete("/{product_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete product")
async def delete_product(product_id: int):
    return f"Delete {product_id} product"


@router.post("/buy/{product_id}")
async def buy_product(product_id: int):
    return f"Purchase <{product_id}> completed"
