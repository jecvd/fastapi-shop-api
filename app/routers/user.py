
from fastapi import APIRouter, status, Depends,HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models import User
from app.schemas import UserOut, UserCreate, Token, UserLogin

router = APIRouter(prefix="/api/users",tags=["用户"])

@router.post("/register",response_model=UserOut,status_code=status.HTTP_201_CREATED)
def register(
        user_data:UserCreate,
        db:Session = Depends(get_db)
):
    if db.query(User).filter(User.username==user_data.username).first():
        raise HTTPException(status_code=400,detail="用户名已被注册")

    if db.query(User).filter(User.email==user_data.email).first():
        raise HTTPException(status_code=400,detail="邮箱已被注册")

    user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login",response_model=Token)
def login(
        user_data:UserLogin,
        db:Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(status_code=400,detail="用户名或密码错误")

    if not verify_password(user_data.password,user.hashed_password):
        raise HTTPException(status_code=400,detail="用户名或密码错误")

    token = create_access_token(data={"sub":user.username})
    return {"access_token":token,"token_type":"bearer"}

