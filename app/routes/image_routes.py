from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.database import get_db
from app.models.image import Image
from app.utils.image_utils import save_image, validate_image
from app.utils.model_utils import analyze_image_with_qwen
from app.utils.response_utils import success_response, error_response
import logging
from pydantic import BaseModel, validator
from typing import Optional, List
import pandas as pd
from fastapi.responses import StreamingResponse
import io

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
    try:
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
        
        # 合并分析结果
        logger.info("开始合并分析结果")
        # 先从正面图片获取价格
        front_price = front_analysis.get("price", 0) if front_analysis else 0
        # 如果正面图片价格无效，尝试从背面图片获取
        back_price = back_analysis.get("price", 0) if back_analysis else 0
        
        # 确定最终价格
        final_price = 0
        if front_price and front_price != "N/A" and front_price != "":
            try:
                final_price = float(front_price)
            except ValueError:
                # 如果正面图片价格无效，尝试使用背面图片价格
                if back_price and back_price != "N/A" and back_price != "":
                    try:
                        final_price = float(back_price)
                    except ValueError:
                        final_price = 0
                else:
                    final_price = 0
        else:
            # 正面图片价格无效，尝试使用背面图片价格
            if back_price and back_price != "N/A" and back_price != "":
                try:
                    final_price = float(back_price)
                except ValueError:
                    final_price = 0
            else:
                final_price = 0
        
        merged_result = {
            "brand": front_analysis.get("brand", "N/A") if front_analysis else "N/A",
            "name": front_analysis.get("name", "N/A") if front_analysis else "N/A",
            "price": final_price,
            "barcode": back_analysis.get("barcode", "N/A") if back_analysis else "N/A"
        }
        logger.info(f"合并结果: {merged_result}")
           
        result = {
            # "id": db_image.id,
            "front_image_path": front_path,
            "back_image_path": back_path,
            "front_analysis": front_analysis,
            "back_analysis": back_analysis,
            "merged_result": merged_result
        }
        logger.info("请求处理完成")
        return success_response(result, "Images uploaded successfully")
    except FileNotFoundError as e:
        logger.error(f"文件未找到错误: {e}")
        return error_response(404, f"文件未找到: {str(e)}")
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {e}")
        return error_response(500, f"数据库操作失败: {str(e)}")
    except Exception as e:
        logger.error(f"处理图片上传时发生未知错误: {e}")
        return error_response(500, f"处理图片上传时发生错误: {str(e)}")

@router.options("/upload-images/")
async def options_upload_images():
    # 这个函数只用于处理OPTIONS请求，返回200状态码
    return {"status": "OK"}


# 查询Image表（支持分页）
@router.post("/images/")
async def get_all_images(
    page: int = Query(1, ge=1, description="页码，默认为1"),
    page_size: int = Query(10, ge=1, le=100, description="每页数据量，默认为10，最大为100"),
    db: Session = Depends(get_db)
):
    try:
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 查询分页数据
        images = db.query(Image).offset(offset).limit(page_size).all()
        
        # 获取总数据量
        total = db.query(Image).count()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        # 构造返回数据
        result = {
            "data": images,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "total_items": total
            }
        }
        
        return success_response(result, "成功获取图像数据")
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {e}")
        return error_response(500, f"数据库操作失败: {str(e)}")
    except Exception as e:
        logger.error(f"获取图像数据时发生未知错误: {e}")
        return error_response(500, f"获取图像数据时发生错误: {str(e)}")


# 定义更新图像信息的请求模型
class ImageUpdateRequest(BaseModel):
    front_image_path: Optional[str] = None
    back_image_path: Optional[str] = None
    brand: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    barcode: Optional[str] = None
    quantity: Optional[int] = None
    operationType: Optional[str] = None
    
    @validator('price', pre=True)
    def validate_price(cls, v):
        if v is None:
            return 0.0
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                return 0.0
        return float(v)
    
    @validator('quantity', pre=True)
    def validate_quantity(cls, v):
        if v is None:
            return 0
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                return 0
        return int(v)

@router.post("/update-image")
async def update_image_info(
    request: ImageUpdateRequest,
    db: Session = Depends(get_db)
):
    try:
        # 根据barcode更新或新增数据
        logger.info(f"开始根据barcode更新或新增数据: {request.barcode}")
        
        # 查找是否已存在该barcode的记录
        existing_image = db.query(Image).filter(Image.barcode == request.barcode).first()
        
        if existing_image:
            # 如果存在，则根据operationType更新number字段和price字段
            logger.info(f"找到已存在的记录，ID: {existing_image.id}，更新number和price字段")
            if request.quantity is not None:
                if request.operationType == "1":
                    # 增加数量
                    current_number = int(existing_image.number) if existing_image.number else 0
                    existing_image.number = str(current_number + request.quantity)
                else:
                    # 直接设置数量
                    existing_image.number = str(request.quantity)
            
            # 更新price字段
            if request.price is not None:
                existing_image.price = request.price
            
            db.commit()
            db.refresh(existing_image)
            logger.info(f"数据库更新完成，记录ID: {existing_image.id}")
            return success_response(existing_image, "图像信息更新成功")
        else:
            # 如果不存在，则新增一条数据
            logger.info("未找到已存在的记录，新增一条数据")
            new_image = Image(
                front_image_path=request.front_image_path if request.front_image_path is not None else "",
                back_image_path=request.back_image_path if request.back_image_path is not None else "",
                brand=request.brand if request.brand is not None else "",
                name=request.name if request.name is not None else "",
                price=request.price if request.price is not None else 0,
                barcode=request.barcode if request.barcode is not None else "",
                number=str(request.quantity) if request.quantity is not None else "0"
            )
            db.add(new_image)
            db.commit()
            db.refresh(new_image)
            logger.info(f"数据库新增完成，记录ID: {new_image.id}")
            return success_response(new_image, "新图像信息创建成功")
    except FileNotFoundError as e:
        logger.error(f"文件未找到错误: {e}")
        db.rollback()
        return error_response(404, f"文件未找到: {str(e)}")
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {e}")
        db.rollback()
        return error_response(500, f"数据库操作失败: {str(e)}")
    except Exception as e:
        logger.error(f"更新图像信息时发生未知错误: {e}")
        db.rollback()
        return error_response(500, f"更新图像信息时发生错误: {str(e)}")


# 导出Image表为Excel文件
@router.get("/export-images/")
async def export_images_to_excel(db: Session = Depends(get_db)):
    try:
        # 查询所有图像数据
        images = db.query(Image).all()
        
        # 将数据转换为字典列表
        data = []
        for image in images:
            data.append({
                "ID": image.id,
                "正面图片路径": image.front_image_path,
                "背面图片路径": image.back_image_path,
                "品牌": image.brand,
                "名称": image.name,
                "价格": image.price,
                "条形码": image.barcode,
                "数量": image.number,
                "创建时间": image.created_at,
                "更新时间": image.updated_at
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 将DataFrame写入字节流
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Images')
        output.seek(0)
        
        # 返回StreamingResponse
        headers = {
            'Content-Disposition': 'attachment; filename="images.xlsx"'
        }
        return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    except Exception as e:
        logger.error(f"导出Excel时发生未知错误: {e}")
        return error_response(500, f"导出Excel时发生错误: {str(e)}")