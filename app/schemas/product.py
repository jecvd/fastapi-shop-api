from datetime import datetime

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name:str = Field(...,max_length=100,description = "商品名称")
    price:float = Field(...,ge=1,description = "价格")
    description: str | None = None
    category: str | None = None
    stock:int = Field(...,ge=0,description = "库存")

class ProductUpdate(BaseModel):
    name: str | None = Field(None, max_length=100, description="商品名称")
    price: float | None = Field(None, ge=1, description="价格")
    description: str | None = Field(None, description="商品描述")
    stock: int | None = Field(None, ge=0, description="库存")
    category: str | None = Field(None, description="分类")
    is_active: bool | None = Field(None, description="是否上架")

class ProductOut(BaseModel):
    id:int
    name:str
    description:str|None
    price:float
    stock:int
    category:str|None
    is_active:bool
    created_at:datetime
    updated_at:datetime

    class Config():
        from_attributes = True