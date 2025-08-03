# Image Processing API

这是一个使用FastAPI和SQLite构建的后端系统，用于接收和处理正面和反面图片。

## 功能

- 接收正面和反面两张图片
- 验证图片有效性
- 保存图片到本地
- 将图片信息存储到SQLite数据库

## 技术栈

- FastAPI
- SQLite
- SQLAlchemy
- Pillow (PIL)

## 安装

1. 克隆项目
2. 安装依赖:

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

服务器将在 `http://localhost:8000` 上运行

## API Endpoints

- `POST /api/v1/upload-images/` - 上传正面和反面图片
  - 参数:
    - `front_image`: 正面图片文件
    - `back_image`: 反面图片文件

## 数据库

项目使用SQLite数据库，数据库文件将自动创建为 `app.db`

## 上传的图片

上传的图片将保存在 `uploads/` 目录中