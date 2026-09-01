from datetime import datetime

from sqlalchemy import Numeric, String, DateTime, Integer,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.core.database import Base
from app.models.product import Product


class Order(Base):
    __tablename__ = "orders"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"),index=True)
    total_amount:Mapped[float] = mapped_column(Numeric(10,2),default=0)
    status:Mapped[str] = mapped_column(String(20),default="pending")
    created_at:Mapped[datetime] = mapped_column(DateTime,default=datetime.now)
    items:Mapped[list["OrderItem"]] = relationship(back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    order_id:Mapped[int] = mapped_column(ForeignKey("orders.id"),index=True)
    product_id:Mapped[int] = mapped_column(ForeignKey("products.id"),index=True)
    quantity:Mapped[int] = mapped_column(Integer,default=1)
    price:Mapped[float] = mapped_column(Numeric(10,2))
    order:Mapped["Order"] = relationship(back_populates="items")
    product:Mapped["Product"] = relationship()