import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.models import User, Product, Order, OrderItem

# 测试数据库连接（独立的库，不污染开发数据）
TEST_DATABASE_URL = "mysql+pymysql://root:12345678@localhost:3306/shop_test?charset=utf8mb4"
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """把 app 的 get_db 依赖替换成测试数据库的会话"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 替换依赖：app 里所有用 Depends(get_db) 的地方，都改用测试数据库
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """测试客户端：每个测试前建空表，测试后删表，保证测试之间互不影响"""
    Base.metadata.create_all(bind=test_engine)   # 建表
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=test_engine)     # 删表


@pytest.fixture
def auth_headers(client):
    """自动注册+登录，返回带 token 的请求头（给需要认证的接口用）"""
    # 注册
    client.post("/api/users/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456"
    })
    # 登录拿 token
    response = client.post("/api/users/login", json={
        "username": "testuser",
        "password": "123456"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
