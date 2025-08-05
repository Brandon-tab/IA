from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.database.database import Base

class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    front_image_path = Column(String, nullable=False)
    back_image_path = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    name = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    barcode = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)