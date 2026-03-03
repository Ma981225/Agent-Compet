"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API配置
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# 模型服务配置（由判题器下发）
MODEL_IP = os.getenv("MODEL_IP", "localhost")
MODEL_PORT = int(os.getenv("MODEL_PORT", "8888"))
MODEL_BASE_URL = f"http://{MODEL_IP}:{MODEL_PORT}"

# 兼容旧配置
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", MODEL_BASE_URL)

# Web服务配置
SERVER_HOST = os.getenv("HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("PORT", "8000"))

# 模型配置
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# 房源平台配置
PLATFORMS = ["lianjia", "anjuke", "58tongcheng"]

# 评价权重配置
WEIGHTS = {
    "commute": 0.3,  # 通勤距离权重
    "price_ratio": 0.4,  # 租金性价比权重
    "facilities": 0.3,  # 生活配套权重
}

# 最大候选房源数
MAX_CANDIDATES = 5
