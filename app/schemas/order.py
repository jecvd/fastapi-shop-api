from datetime import datetime

from pydantic import BaseModel, Field



class OrderItemCreate(BaseModel):
    product_id:int = Field(...,description="要买那个商品")
    quantity:int =Field(...,ge=1)

class OrderCreate(BaseModel):
    items:list[OrderItemCreate] = Field(...,description="商品订单列表")

class OrderItemOut(BaseModel):
    id:int
    product_id:int
    order_id:int
    quantity:int
    price:float
    product_name:str

    class Config():
        from_attributes = True

class OrderOut(BaseModel):
    id:int
    user_id:int
    total_amount:float
    status:str
    created_at:datetime
    items:list[OrderItemOut]

    class Config():
        from_attributes = True
