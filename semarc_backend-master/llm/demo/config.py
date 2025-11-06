import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env文件

class QwenConfig:
    API_KEY = os.getenv("DASHSCOPE_API_KEY")  # 从.env读取
    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    MODEL = "qwen2.5-14b-instruct-1m"  # 可选模型：qwen-turbo, qwen-max等