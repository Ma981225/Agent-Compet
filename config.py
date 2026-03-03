"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API配置
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")

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
