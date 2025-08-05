import json
import base64
import os
import re
from typing import Dict, Any, Optional
import dashscope
from dashscope import MultiModalConversation
from dotenv import load_dotenv
from PIL import Image
import io

# 加载.env文件中的环境变量
load_dotenv()
print(f"Model utils DASHSCOPE_API_KEY: {os.getenv('DASHSCOPE_API_KEY')}")

# 配置dashscope API密钥
print(f"Model utils DASHSCOPE_API_KEY: {os.getenv('DASHSCOPE_API_KEY')}")
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    raise ValueError("请设置DASHSCOPE_API_KEY环境变量")


# 重试机制配置
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
TIMEOUT = 120  # 超时时间（秒）


def analyze_image_with_qwen(image_path: str) -> Optional[Dict[str, Any]]:
    """
    使用通义千问VL-Plus大模型分析图片，提取商品信息
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        包含商品信息的字典，包括品牌、名称、价格和条形码
    """
    try:
        # 读取并压缩图片
        with Image.open(image_path) as img:
            # 压缩图片到最大边长为1024像素
            max_size = 1024
            width, height = img.size
            if width > max_size or height > max_size:
                if width > height:
                    new_width = max_size
                    new_height = int(height * max_size / width)
                else:
                    new_height = max_size
                    new_width = int(width * max_size / height)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # 将压缩后的图片转换为base64编码
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # 构造请求内容
        messages = [
            {
                'role': 'user',
                'content': [
                    {'image': f'data:image/jpeg;base64,{encoded_image}'},
                    {'text': '请分析这张商品图片，提取以下信息：品牌、商品名称、价格（如果有）、条形码（如果有）。以JSON格式返回结果，格式如下：{"brand": "品牌", "name": "商品名称", "price": "价格", "barcode": "条形码"} 如果某些信息无法识别，请在对应字段中填入"N/A"。'}
                ]
            }
        ]
        
        # 调用dashscope API
        resp = None
        for attempt in range(MAX_RETRIES):
            try:
                print(f"开始第 {attempt + 1} 次API调用")
                resp = MultiModalConversation.call(
                    model='qwen-vl-plus',
                    messages=messages,
                    timeout=TIMEOUT
                )
                print(f"第 {attempt + 1} 次API调用完成，状态码: {resp.status_code}")
                if resp.status_code == 200:
                    break
            except Exception as e:
                print(f"API调用失败（尝试 {attempt + 1}/{MAX_RETRIES}）: {e}")
                if attempt < MAX_RETRIES - 1:
                    import time
                    time.sleep(BACKOFF_FACTOR * (2 ** attempt))  # 指数退避
                else:
                    raise e
        
        # 检查响应状态
        if resp.status_code == 200:
            # 处理响应数据结构
            response_content = resp.output.choices[0].message.content
            print(f"API调用成功，响应内容: {response_content}")
            
            # 如果响应内容是列表，提取第一个元素的text字段
            if isinstance(response_content, list) and len(response_content) > 0:
                output_text = response_content[0].get('text', '')
            else:
                output_text = response_content
        else:
            print(f"API调用失败，状态码: {resp.status_code}")
            print(f"错误信息: {resp.message}")
            print(f"完整响应: {resp}")
            raise Exception(f"API调用失败，状态码: {resp.status_code}, 错误信息: {resp.message}")
        
        # 尝试解析JSON
        try:
            # 提取JSON部分，处理可能的代码块标记
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', output_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            
            # 如果没有代码块标记，尝试直接提取JSON
            json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回原始响应
            return {"raw_response": output_text}
            
    except Exception as e:
        print(f"Error analyzing image with Qwen: {e}")
        return None