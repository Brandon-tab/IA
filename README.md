# Image Processing API

这是一个功能完整的图像处理和管理系统，使用FastAPI和SQLite构建。系统能够接收和处理正面和反面图片，利用通义千问VL-Plus AI模型进行图像分析，并提供Web界面进行数据管理和Excel导出功能。

## 主要功能

- 接收正面和反面两张图片
- 验证图片有效性
- 保存图片到本地
- 使用AI模型分析图片内容
- 将图片信息存储到SQLite数据库
- 提供Web界面查看和管理图像数据
- 支持将图像数据导出为Excel文件
- 支持数据分页显示

## 技术栈

### 后端
- FastAPI (v0.68.0) - 用于构建API接口
- Uvicorn (v0.15.0) - ASGI服务器
- SQLite - 作为数据库存储图像信息
- SQLAlchemy (v1.4.23) - ORM框架，用于数据库操作
- Pillow (v8.3.1) - 图像处理库
- DashScope (通义千问VL-Plus v1.14.0) - AI图像分析服务
- Pandas (v1.3.3) - 数据处理和Excel导出
- XlsxWriter (v3.0.2) - Excel文件生成
- Transformers (v4.46.3) - AI模型处理
- PyTorch (v2.4.1) - 机器学习框架
- Requests (v2.25.1) - HTTP客户端
- python-multipart (v0.0.5) - 处理multipart请求
- python-dotenv (v0.19.0) - 环境变量加载

### 前端

#### PC管理端
- Vue 3 (v3.5.18) - 渐进式JavaScript框架
- Element Plus (v2.10.5) - Vue 3组件库
- Vite (v7.0.6) - 前端构建工具
- Axios (v1.7.9) - HTTP客户端
- Pinia (v3.0.3) - Vue状态管理
- Vue Router (v4.5.1) - Vue路由管理

#### 移动端
- Vue 3 (v3.2.41) - 渐进式JavaScript框架
- Vant (v4.9.21) - 移动端Vue组件库
- Vite (v3.1.8) - 前端构建工具
- Pinia (v2.0.23) - Vue状态管理
- Vue Router (v4.1.5) - Vue路由管理

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

### 后端

```bash
python main.py
```

服务器将在 `http://localhost:8001` 上运行

### 前端

进入前端目录并安装依赖:

```bash
cd frontend/pc-admin
npm install
```

运行开发服务器:

```bash
npm run dev
```

前端将在 `http://localhost:5173` 上运行

## 超时设置

后端接口默认设置为2分钟超时时间，以确保有足够的时间处理图片上传和分析。

## Excel导出功能

系统支持将所有图像数据导出为Excel文件。在PC管理端的图像数据表页面，点击"导出Excel"按钮即可下载包含所有图像信息的Excel文件。

导出的Excel文件包含以下字段:
- ID: 图像记录ID
- 正面图片路径: 正面图片存储路径
- 背面图片路径: 背面图片存储路径
- 品牌: 图像识别出的品牌
- 名称: 图像识别出的名称
- 价格: 图像识别出的价格
- 条形码: 图像识别出的条形码
- 数量: 商品数量
- 创建时间: 记录创建时间
- 更新时间: 记录更新时间

## API Endpoints

- `POST /api/v1/upload-images/` - 上传正面和反面图片
  - 参数:
    - `front_image`: 正面图片文件
    - `back_image`: 反面图片文件
  - 响应:
    - `front_analysis`: 正面图片分析结果
    - `back_analysis`: 反面图片分析结果

- `POST /images/` - 获取图像数据列表（支持分页）
  - 参数:
    - `page`: 页码（默认为1）
    - `page_size`: 每页数据量（默认为10，最大为100）
  - 响应:
    - `data`: 图像数据列表
    - `pagination`: 分页信息

- `GET /export-images/` - 导出所有图像数据为Excel文件
  - 响应:
    - Excel文件下载

## 项目结构

```
IA/
├── app/                 # 后端应用目录
│   ├── database/        # 数据库配置
│   ├── models/          # 数据模型
│   ├── routes/          # API路由
│   ├── utils/           # 工具函数
│   └── app.db           # SQLite数据库文件
├── frontend/            # 前端应用目录
│   ├── pc-admin/        # PC管理端
│   │   ├── src/         # 源代码目录
│   │   └── package.json # 依赖配置文件
│   └── mobile-app/      # 移动端应用
│       ├── src/         # 源代码目录
│       └── package.json # 依赖配置文件
├── uploads/             # 上传图片存储目录
├── main.py              # 后端应用入口
├── requirements.txt     # 后端依赖文件
└── README.md            # 项目说明文件
```

## 数据库

项目使用SQLite数据库，数据库文件将自动创建为 `app.db`

## 上传的图片

上传的图片将保存在 `uploads/` 目录中