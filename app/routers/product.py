from typing import List

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Product
from app.schemas import ProductOut, ProductCreate, ProductUpdate
from app.core.cache import get_product_with_rebuild, delete_cached


router = APIRouter(prefix="/api/products",tags=["商品"])

@router.post("/",response_model=ProductOut,status_code=status.HTTP_201_CREATED)
def create_product(
        product_data : ProductCreate,
        db:Session = Depends(get_db)
):
    if db.query(Product).filter(Product.name==product_data.name).first():
        raise HTTPException(status_code=400,detail="商品已存在")
    product = Product(
        name = product_data.name,
        price = product_data.price,
        description = product_data.description,
        category = product_data.category,
        stock = product_data.stock
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.get("/",response_model=List[ProductOut])
def get_products(
        skip:int = 0,
        limit:int = 10,
        db:Session = Depends(get_db)
):
    return db.query(Product).offset(skip).limit(limit).all()

@router.get("/{product_id}",response_model=ProductOut)
def get_product(
        product_id:int,
        db:Session = Depends(get_db)
):
    def db_query(pid):
        return db.query(Product).filter(Product.id==pid).first()
    data = get_product_with_rebuild(product_id,db_query)
    if data is None:
        raise HTTPException(status_code=404,detail="商品不存在")
    if isinstance(data,dict):
        return ProductOut(**data)
    return data

@router.put("/{product_id}",response_model=ProductOut)
def update_product(
        product_id:int,
        product_data:ProductUpdate,
        db:Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.id==product_id).first()
    if not db_product:
        raise HTTPException(status_code=404,detail="商品不存在")
    if product_data.name is not None:
        db_product.name = product_data.name
    if product_data.price is not None:
        db_product.price = product_data.price
    if product_data.description is not None:
        db_product.description = product_data.description
    if product_data.category is not None:
        db_product.category = product_data.category
    if product_data.stock is not None:
        db_product.stock = product_data.stock
    if product_data.is_active is not None:
        db_product.is_active = product_data.is_active

    db.commit()
    db.refresh(db_product)
    delete_cached(f"product:{product_id}")
    return db_product

@router.delete("/{product_id}")
def delete_product(
        product_id :int,
        db:Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="商品不存在")
    db.delete(product)
    db.commit()
    delete_cached(f"product:{product_id}")
    return {"detail": "删除成功"}







