from app.core.database import Base, engine
import app.models

Base.metadata.create_all(bind=engine)
print("数据表创建成功")