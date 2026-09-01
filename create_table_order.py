from app.core.database import Base, engine
from app.models.order import Order,OrderItem

Base.metadata.create_all(bind=engine)