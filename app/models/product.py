from datetime import datetime

from sqlalchemy import String, Text, Numeric, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(100),unique=True,nullable=False,index=True,comment="商品名称")
    description:Mapped[str|None] = mapped_column(Text,nullable=True,comment="商品描述")
    price:Mapped[float] = mapped_column(Numeric(10, 2),nullable=False,comment="价格")
    stock:Mapped[int] = mapped_column(Integer,default=0,comment="库存")
    version:Mapped[int] = mapped_column(Integer,default=0,comment="乐观锁版本号")
    category:Mapped[str|None] = mapped_column(String(50),nullable=True,index=True,comment="分类")
    is_active:Mapped[bool] = mapped_column(Boolean,default=True,comment="是否上架")
    created_at:Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment="创建时间")
    updated_at:Mapped[datetime] = mapped_column(DateTime,default=datetime.now,onupdate=datetime.now,comment="更新时间")