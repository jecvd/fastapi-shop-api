from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Order, Product, OrderItem, User
from app.schemas import OrderOut, OrderCreate

router = APIRouter(prefix="/api/orders",tags=["订单"])

@router.post("/",response_model=OrderOut)
def create_order(
        order_data:OrderCreate,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)
):
    total = 0
    order_items = []
    for db_order in order_data.items:
        product = db.query(Product).filter(Product.id == db_order.product_id).first()
        if not product:
            raise HTTPException(status_code=400,detail="商品不存在")
        if product.stock < db_order.quantity:
            raise HTTPException(400,f"商品{product.name}库存不足")
        #减库存
        product.stock = product.stock - db_order.quantity
        #算这一项的总金额
        total = total + db_order.quantity * product.price
        #把明细收集起来，先不commit
        order_items.append(OrderItem(
                product_id = db_order.product_id,
                quantity = db_order.quantity,
                price = product.price
            )
        )

    order = Order(
        user_id = current_user.id,
        total_amount = total
    )

    order.items = order_items

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in order.items:
        item.product_name = item.product.name

    return order

@router.get("/",response_model=List[OrderOut])
def get_orders(
        skip:int = 0,
        limit:int = 10,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    for order in orders:
        for item in order.items:
            item.product_name = item.product.name

    return orders

@router.get("/{order_id}",response_model=OrderOut)
def get_order(
        order_id:int,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)
):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404,detail="订单不存在")
    if db_order.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="无权查看该订单")
    for item in db_order.items:
        item.product_name = item.product.name
    return db_order

