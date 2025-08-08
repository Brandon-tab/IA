from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.database.database import Base
from pydantic import BaseModel


class ImageBase(BaseModel):
    id: int
    front_image_path: str
    back_image_path: str
    brand: str = None
    name: str = None
    price: float = None
    barcode: str = None
    number: str = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    front_image_path = Column(String, nullable=False)
    back_image_path = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    name = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    barcode = Column(String, nullable=True)
    number = Column(String, nullable=True)  # 新增的number字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)