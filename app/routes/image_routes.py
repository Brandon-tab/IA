from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.image import Image
from app.utils.image_utils import save_image, validate_image

router = APIRouter()

@router.post("/upload-images/")
async def upload_images(
    front_image: UploadFile = File(...),
    back_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 保存图片
    front_path = save_image(front_image, "front")
    back_path = save_image(back_image, "back")
    
    # 保存到数据库
    db_image = Image(front_image_path=front_path, back_image_path=back_path)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    return {
        "message": "Images uploaded successfully",
        "id": db_image.id,
        "front_image_path": front_path,
        "back_image_path": back_path
    }

@router.options("/upload-images/")
async def options_upload_images():
    # 这个函数只用于处理OPTIONS请求，返回200状态码
    return {"status": "OK"}