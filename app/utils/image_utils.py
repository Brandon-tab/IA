import os
from PIL import Image as PILImage
import uuid
from typing import Tuple

# 获取当前文件所在的目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# 确保上传目录存在
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_image(image_file, prefix: str) -> str:
    """保存上传的图片并返回保存路径"""
    # 生成唯一文件名
    filename = f"{prefix}_{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # 保存图片
    with PILImage.open(image_file.file) as img:
        # 转换为RGB模式以确保兼容性
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(file_path, format='JPEG', quality=85)
    
    return file_path

def validate_image(image_file) -> Tuple[bool, str]:
    """验证上传的文件是否为有效图片"""
    try:
        with PILImage.open(image_file.file) as img:
            img.verify()
        image_file.file.seek(0)  # 重置文件指针
        return True, "Valid image"
    except Exception as e:
        return False, str(e)