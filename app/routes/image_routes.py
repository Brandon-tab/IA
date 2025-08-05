from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.image import Image
from app.utils.image_utils import save_image, validate_image
from app.utils.model_utils import analyze_image_with_qwen
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload-images/")
async def upload_images(
    front_image: UploadFile = File(...),
    back_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    logger.info("开始处理图片上传请求")
    
    # 保存图片
    logger.info("开始保存图片")
    front_path = save_image(front_image, "front")
    back_path = save_image(back_image, "back")
    logger.info(f"图片保存完成，正面图片路径: {front_path}, 背面图片路径: {back_path}")
    
    # 保存到数据库
    logger.info("开始保存到数据库")
    db_image = Image(front_image_path=front_path, back_image_path=back_path)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    logger.info(f"数据库保存完成，记录ID: {db_image.id}")
    
    # 分析图片
    logger.info("开始分析正面图片")
    front_analysis = analyze_image_with_qwen(front_path)
    logger.info("开始分析背面图片")
    back_analysis = analyze_image_with_qwen(back_path)
    logger.info("图片分析完成")
    
    result = {
        "message": "Images uploaded successfully",
        "id": db_image.id,
        "front_image_path": front_path,
        "back_image_path": back_path,
        "front_analysis": front_analysis,
        "back_analysis": back_analysis
    }
    logger.info("请求处理完成")
    return result

@router.options("/upload-images/")
async def options_upload_images():
    # 这个函数只用于处理OPTIONS请求，返回200状态码
    return {"status": "OK"}