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
- DashScope (通义千问VL-Plus)

## 安装

1. 克隆项目
2. 安装依赖:

```bash
pip install -r requirements.txt
```

## 配置

在使用图片分析功能之前，需要设置DashScope API密钥:

### Windows (命令提示符)
```cmd
set DASHSCOPE_API_KEY=your_api_key_here
```

### Windows (PowerShell)
```powershell
$env:DASHSCOPE_API_KEY="your_api_key_here"
```

### macOS/Linux
```bash
export DASHSCOPE_API_KEY=your_api_key_here
```

## 运行

```bash
python main.py
```

服务器将在 `http://localhost:8001` 上运行

## 超时设置

后端接口默认设置为2分钟超时时间，以确保有足够的时间处理图片上传和分析。

## API Endpoints

- `POST /api/v1/upload-images/` - 上传正面和反面图片
  - 参数:
    - `front_image`: 正面图片文件
    - `back_image`: 反面图片文件
  - 响应:
    - `front_analysis`: 正面图片分析结果
    - `back_analysis`: 反面图片分析结果

## 数据库

项目使用SQLite数据库，数据库文件将自动创建为 `app.db`

## 上传的图片

上传的图片将保存在 `uploads/` 目录中