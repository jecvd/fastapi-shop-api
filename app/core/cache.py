from app.core.config import REDIS_URL

from redis import Redis
import random
import json
import threading

cache = Redis.from_url(REDIS_URL,decode_responses=True,protocol = 2)

def product_to_dict(p) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": float(p.price),          # Numeric 是 Decimal，转 float
        "stock": p.stock,
        "category": p.category,
        "is_active": p.is_active,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }

def get_cached(key:str) -> str|None:
    return cache.get(key)
def set_cached(key:str,value:str,ttl:int) ->None:
    cache.set(key,value,ex=ttl)
def delete_cached(*keys:str,) ->None:
    cache.delete(*keys)

BASE_TTL = 300
JITTER = 60
def random_ttl()->int:
    return BASE_TTL + random.randint(0,JITTER)

EMPTY = ""
def serialize(obj) -> str:
    return json.dumps(obj,ensure_ascii=False,default=str)

def get_product_from_cache(product_id:int):
    raw = get_cached(f"product:{product_id}")
    if raw is None:
        return None,False
    if raw == EMPTY:
        return None,True
    return json.loads(raw),True

_rebuild_lock = threading.Lock()

def get_product_with_rebuild(product_id:int,db_query):
    data,hit = get_product_from_cache(product_id)
    if hit:
        return data
    with _rebuild_lock:
        data,hit = get_product_from_cache(product_id)
        if hit:
            return data

        product = db_query(product_id)
        if product is None:
            set_cached(f"product:{product_id}",EMPTY,60)
            return None
        set_cached(f"product:{product_id}",serialize(product_to_dict(product)),random_ttl())
        return product

