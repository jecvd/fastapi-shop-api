# 数据库连接
DATABASE_URL = "mysql+pymysql://root:12345678@localhost:3306/shop?charset=utf8mb4"

REDIS_URL = "redis://localhost:6379/0"

# JWT 配置（用户模块会用到，先写好）
SECRET_KEY = "xgfdxjnfgfhxdrhxdr"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # token 24 小时后过期

