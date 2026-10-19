import os
from fastapi import FastAPI, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgrespassword@db:5432/appdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DeviceModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IoT & Network Devices Monitoring API",
    description="""
    ### Лабораторна робота №1 з дисципліни «Хмарні технології»
    **Виконавець:** студент гр. ІР-23 Роман Коцур  
    **Стек:** FastAPI, PostgreSQL (RDS), Docker, AWS ECS Fargate, Terraform.
    """,
    version="1.0.1",
    contact={
        "name": "Роман Коцур",
        "email": "r.kotsur@lpnu.ua",
    },
)

class ItemCreate(BaseModel):
    name: str = Field(
        ..., 
        title="Назва пристрою", 
        json_schema_extra={"example": "ESP32 Moisture Monitor"}
    )
    description: str | None = Field(
        None, 
        title="Опис або локація", 
        json_schema_extra={"example": "Subnet 10.0.1.0/24 - Zone A"}
    )

class ItemResponse(ItemCreate):
    id: int = Field(..., title="ID запису в БД", json_schema_extra={"example": 1})

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get(
    "/health", 
    tags=["Mониторинг"], 
    summary="Перевірка стану (Health Check)",
    description="Ендпоінт для перевірки працездатності контейнера балансувальником AWS ALB."
)
def health_check():
    return {"status": "ok", "service": "IoT Monitoring API"}

@app.get(
    "/items", 
    response_model=list[ItemResponse], 
    tags=["Пристрої"], 
    summary="Отримати список усіх зареєстрованих пристроїв"
)
def get_items(db: Session = Depends(get_db)):
    return db.query(DeviceModel).all()

@app.post(
    "/items", 
    response_model=ItemResponse, 
    status_code=status.HTTP_201_CREATED, 
    tags=["Пристрої"], 
    summary="Зареєструвати новий пристрій у базі даних"
)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemModel(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item