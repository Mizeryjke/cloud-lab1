import os
import json
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import redis

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgrespassword@localhost:5432/appdb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

class ItemCreate(BaseModel):
    name: str
    description: str | None = None

class ItemResponse(ItemCreate):
    id: int
    class Config:
        from_attributes = True

app = FastAPI(title="Cloud Lab 2 API", version="2.1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    redis_status = "ok"
    try:
        cache.ping()
    except Exception:
        redis_status = "unreachable"
    return {"status": "ok", "redis": redis_status}

@app.get("/items", response_model=List[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    cache_key = "all_items"
    
    try:
        cached_data = cache.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except Exception:
        pass

    items = db.query(ItemModel).all()
    result = [{"id": item.id, "name": item.name, "description": item.description} for item in items]
    
    try:
        cache.setex(cache_key, 40, json.dumps(result))
    except Exception:
        pass

    return result

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(None, alias="Idempotency-Key")
):
    
    if idempotency_key:
        redis_idemp_key = f"idempotency:{idempotency_key}"
        try:
            cached_response = cache.get(redis_idemp_key)
            if cached_response:
                return json.loads(cached_response)
        except Exception:
            pass

    db_item = ItemModel(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    result = {"id": db_item.id, "name": db_item.name, "description": db_item.description}

    if idempotency_key:
        try:
            cache.setex(f"idempotency:{idempotency_key}", 86400, json.dumps(result))
        except Exception:
            pass

    try:
        cache.delete("all_items")
    except Exception:
        pass

    return result