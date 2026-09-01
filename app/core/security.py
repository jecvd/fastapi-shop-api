from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.core.database import get_db
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash_password(password:str)->str:
    """把明文密码加密成哈希值"""
    return pwd_context.hash(password)

def verify_password(plain_password:str,hash_password:str)->bool:
    """登录时校验密码是否正确"""
    return pwd_context.verify(plain_password,hash_password)

# ===== 新增：生成 JWT token =====
def create_access_token(data:dict)->str:
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/users/login")

def get_current_user(
        token:str = Depends(oauth2_scheme),
        db:Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    except:
        raise HTTPException(status_code=401,detail="解码失败")
    username = payload.get("sub")
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=401,detail="用户不存在")
    return user



