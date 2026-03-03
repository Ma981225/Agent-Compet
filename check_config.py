"""
检查配置是否正确
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("配置检查")
print("=" * 60)

# 检查.env文件
env_file = ".env"
if os.path.exists(env_file):
    print(f"✓ .env 文件存在: {env_file}")
else:
    print(f"✗ .env 文件不存在: {env_file}")
    print("  请创建.env文件并配置以下内容：")
    print("  OPENAI_API_KEY=your_api_key_here")
    print("  OPENAI_BASE_URL=https://api.openai.com/v1")
    print("  MODEL_NAME=gpt-3.5-turbo")
    print()

# 检查关键配置
configs = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", ""),
    "MODEL_NAME": os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
    "API_BASE_URL": os.getenv("API_BASE_URL", "http://localhost:8000"),
    "SERVER_HOST": os.getenv("HOST", "0.0.0.0"),
    "SERVER_PORT": os.getenv("PORT", "8000"),
}

print("\n配置项检查:")
print("-" * 60)

for key, value in configs.items():
    if key == "OPENAI_API_KEY":
        if value:
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"✓ {key}: {masked_value}")
        else:
            print(f"✗ {key}: 未设置（必需）")
    else:
        status = "✓" if value else "✗"
        print(f"{status} {key}: {value if value else '未设置'}")

print("-" * 60)

# 检查OpenAI配置
if not configs["OPENAI_API_KEY"]:
    print("\n⚠️  警告: OPENAI_API_KEY 未配置！")
    print("\n请按以下步骤配置：")
    print("1. 在项目根目录创建 .env 文件")
    print("2. 添加以下内容：")
    print("   OPENAI_API_KEY=sk-your-api-key-here")
    print("   OPENAI_BASE_URL=https://api.openai.com/v1")
    print("   MODEL_NAME=gpt-3.5-turbo")
    print("\n或者设置环境变量：")
    print("   export OPENAI_API_KEY=sk-your-api-key-here")
else:
    print("\n✓ 配置检查通过！")

print("=" * 60)