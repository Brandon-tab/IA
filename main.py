from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import image_routes
from app.database.database import engine, Base
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

# 调试信息：打印环境变量
import os
print(f"DASHSCOPE_API_KEY: {os.getenv('DASHSCOPE_API_KEY')}")

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Image Processing API", description="API for processing front and back images")

# 添加CORS中间件以解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://192.168.31.235:5174",
    "http://192.168.213.1:5174",
    "http://192.168.174.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_routes.router, prefix="")

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Processing API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)