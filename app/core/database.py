from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import DATABASE_URL

#1.创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo = True
)

#2.会话工厂
SessionLocal = sessionmaker(
    bind = engine,
    autocommit=False,
    autoflush=False
)

# 3. 声明式基类：后面所有数据表模型都要继承它
class Base(DeclarativeBase):
    pass

# 4. 依赖注入：FastAPI 每个请求自动获取会话，用完自动关闭
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()








