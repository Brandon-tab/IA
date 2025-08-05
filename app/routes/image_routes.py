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
    
    # 分析图片
    logger.info("开始分析正面图片")
    front_analysis = analyze_image_with_qwen(front_path)
    logger.info("开始分析背面图片")
    back_analysis = analyze_image_with_qwen(back_path)
    logger.info("图片分析完成")
    
    # 保存到数据库
    logger.info("开始保存到数据库")
    db_image = Image(front_image_path=front_path, back_image_path=back_path)
    db.add(db_image)
    db.commit()
    # 合并分析结果
    logger.info("开始合并分析结果")
    merged_result = {
        "brand": front_analysis.get("brand", "N/A") if front_analysis else "N/A",
        "name": front_analysis.get("name", "N/A") if front_analysis else "N/A",
        "price": front_analysis.get("price", 0) if front_analysis and front_analysis.get("price") != "N/A" else (back_analysis.get("price", 0) if back_analysis and back_analysis.get("price") != "N/A" else 0),
        "barcode": back_analysis.get("barcode", "N/A") if back_analysis else "N/A"
    }
    # 确保price字段为数字类型
    if merged_result["price"] == "N/A" or merged_result["price"] == "":
        merged_result["price"] = 0
    else:
        try:
            merged_result["price"] = float(merged_result["price"])
        except ValueError:
            merged_result["price"] = 0
    logger.info(f"合并结果: {merged_result}")
    
    # 更新数据库记录
    logger.info("开始更新数据库记录")
    db_image.brand = merged_result["brand"]
    db_image.name = merged_result["name"]
    db_image.price = merged_result["price"]
    db_image.barcode = merged_result["barcode"]
    db.commit()
    db.refresh(db_image)
    logger.info(f"数据库更新完成，记录ID: {db_image.id}")
    
    result = {
        "message": "Images uploaded successfully",
        "id": db_image.id,
        "front_analysis": front_analysis,
        "back_analysis": back_analysis,
        "merged_result": merged_result
    }
    logger.info("请求处理完成")
    return result

@router.options("/upload-images/")
async def options_upload_images():
    # 这个函数只用于处理OPTIONS请求，返回200状态码
    return {"status": "OK"}