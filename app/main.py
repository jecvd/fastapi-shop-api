from fastapi import FastAPI

from app.routers import user, product, order

app = FastAPI(title="电商系统 API")

app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)

@app.get("/")
def root():
    return {"message":"欢迎使用电商系统API"}