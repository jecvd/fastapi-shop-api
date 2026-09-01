# 电商后端 API 系统

基于 FastAPI + SQLAlchemy + MySQL 的电商后端系统，实现用户认证、商品管理、订单管理三大模块。

## 技术栈

- **框架**: FastAPI
- **ORM**: SQLAlchemy 2.0（Mapped 类型注解新语法）
- **数据库**: MySQL 8.0
- **认证**: JWT（python-jose）
- **密码加密**: bcrypt（passlib）
- **服务器**: Uvicorn

## 功能特性

### 用户模块
- 用户注册（密码 bcrypt 加密存储）
- 用户登录（签发 JWT Token，有效期 24 小时）

### 商品模块
- 商品创建 / 列表（分页）/ 详情 / 更新（部分更新）/ 删除
- 库存管理

### 订单模块
- 创建订单（事务处理：扣库存 + 生成订单 + 订单明细，失败自动回滚）
- 订单列表（仅查看当前用户自己的订单，按时间倒序）
- 订单详情（权限校验，无法查看他人订单）
- JWT 登录保护，下单自动绑定当前用户

## 项目结构

```
app/
├── core/           # 核心配置
│   ├── config.py       # 数据库连接 + JWT 配置
│   ├── database.py     # 引擎 / 会话 / 依赖注入
│   └── security.py     # 密码加密 / JWT 签发与解析 / 当前用户依赖
├── models/         # 数据库模型（ORM）
│   ├── user.py
│   ├── product.py
│   └── order.py        # Order + OrderItem（一对多关系）
├── schemas/        # Pydantic 模型（请求/响应校验）
│   ├── user.py
│   ├── product.py
│   └── order.py        # 嵌套模型（OrderOut 包含 items 列表）
├── routers/        # 路由（接口层）
│   ├── user.py
│   ├── product.py
│   └── order.py
└── main.py         # 应用入口，挂载路由
```

## 快速开始

### 环境要求
- Python 3.10+
- MySQL 8.0+

### 安装

```bash
# 克隆项目
git clone <你的仓库地址>
cd Python_code

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置数据库

创建 MySQL 数据库：
```sql
CREATE DATABASE shop DEFAULT CHARSET utf8mb4;
```

修改 `app/core/config.py` 中的数据库连接信息：
```python
DATABASE_URL = "mysql+pymysql://root:你的密码@localhost:3306/shop?charset=utf8mb4"
```

### 建表

```bash
python create_tables.py
```

### 启动

```bash
uvicorn app.main:app --reload --port 8001
```

访问 http://127.0.0.1:8001/docs 查看交互式 API 文档。

## API 接口

### 用户
| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/users/register | 用户注册 | 否 |
| POST | /api/users/login | 用户登录（返回 JWT） | 否 |

### 商品
| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/products/ | 创建商品 | 否 |
| GET | /api/products/ | 商品列表（分页） | 否 |
| GET | /api/products/{id} | 商品详情 | 否 |
| PUT | /api/products/{id} | 更新商品 | 否 |
| DELETE | /api/products/{id} | 删除商品 | 否 |

### 订单
| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/orders/ | 创建订单 | 是 |
| GET | /api/orders/ | 我的订单列表 | 是 |
| GET | /api/orders/{id} | 订单详情 | 是 |

> 认证接口需在请求头携带：`Authorization: Bearer <token>`

## 数据库表结构

- **users**: id, username, email, hashed_password, is_active, created_at
- **products**: id, name, description, price, stock, category, is_active, created_at, updated_at
- **orders**: id, user_id（外键）, total_amount, status, created_at
- **order_items**: id, order_id（外键）, product_id（外键）, quantity, price

## 项目亮点

1. **JWT 无状态认证**：登录签发 Token，后续请求携带 Token 验证身份
2. **事务处理**：创建订单时扣库存 + 写订单 + 写明细在同一事务中，异常自动回滚
3. **权限控制**：订单接口区分 401（未登录）和 403（无权限），用户只能查看自己的订单
4. **分层架构**：models / schemas / routers 三层分离，代码结构清晰
5. **SQLAlchemy 2.0 新语法**：使用 Mapped + mapped_column 类型注解
