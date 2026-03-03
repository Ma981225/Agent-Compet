# 运行流程指南

## 一、环境准备

### 1. 检查Python版本
```bash
python --version
# 需要 Python 3.8 或更高版本
```

### 2. 创建虚拟环境（推荐）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

## 二、安装依赖

```bash
pip install -r requirements.txt
```

依赖包包括：
- `openai` - OpenAI API客户端
- `requests` - HTTP请求库
- `pydantic` - 数据验证
- `python-dotenv` - 环境变量管理
- `fastapi` - Web框架
- `uvicorn` - ASGI服务器

## 三、配置环境变量

创建 `.env` 文件（在项目根目录）：

```env
# API配置
API_BASE_URL=http://localhost:8000
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# 模型配置
MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=2000
TEMPERATURE=0.7

# Web服务配置（可选）
HOST=0.0.0.0
PORT=8000
```

**重要**：请将 `OPENAI_API_KEY` 替换为你的实际API密钥。

## 四、启动服务

### 方式1：使用启动脚本（推荐）
```bash
python run_server.py
```

### 方式2：直接运行
```bash
python app.py
```

### 方式3：使用uvicorn命令
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 五、验证服务

### 1. 检查服务状态

启动后，你会看到类似输出：
```
正在启动租房需求匹配智能体API服务...

服务已启动，可通过以下地址访问：
  本地访问: http://127.0.0.1:8000
  本机IP:   http://192.168.x.x:8000
  外部访问: http://<你的公网IP>:8000

API端点：
  聊天接口: POST http://192.168.x.x:8000/v1/chat
  重置接口: POST http://192.168.x.x:8000/v1/reset
  健康检查: GET  http://192.168.x.x:8000/health
  API文档:  http://192.168.x.x:8000/docs

按 Ctrl+C 停止服务
```

### 2. 健康检查

在浏览器访问：
```
http://localhost:8000/health
```

或使用curl：
```bash
curl http://localhost:8000/health
```

应该返回：
```json
{
  "status": "ok",
  "message": "服务正常"
}
```

### 3. 查看API文档

在浏览器访问：
```
http://localhost:8000/docs
```

这会打开 Swagger UI，可以查看和测试所有API端点。

## 六、测试API

### 方式1：使用测试脚本
```bash
python test_api.py
```

### 方式2：使用curl

#### 测试聊天接口
```bash
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"我想在朝阳区租一套两居室\"}"
```

#### 测试重置接口
```bash
curl -X POST "http://localhost:8000/v1/reset" \
  -H "Content-Type: application/json" \
  -d "{}"
```

### 方式3：使用Python代码
```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat",
    json={"message": "我想在朝阳区租一套两居室"}
)
print(response.json())
```

## 七、使用示例

### 示例1：简单查询
```bash
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"我想在朝阳区租房\"}"
```

### 示例2：复杂条件查询
```bash
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"查询海淀+两居+近地铁+电梯+民水民电+预算5000+60平以上的房源\"}"
```

### 示例3：多轮对话
```bash
# 第1轮
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"现在的房子太吵了，想换个安静的地方\"}"

# 第2轮
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"朝阳区，预算6000左右\"}"

# 第3轮
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"两居室，最好近地铁\"}"

# 第4轮 - 搜索房源
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"帮我找找看\"}"
```

## 八、停止服务

按 `Ctrl+C` 停止服务。

## 九、常见问题

### 1. 端口被占用
如果8000端口被占用，可以修改端口：
```bash
# 方式1：设置环境变量
set PORT=8080  # Windows
export PORT=8080  # Linux/Mac
python run_server.py

# 方式2：修改 .env 文件
PORT=8080
```

### 2. 无法访问服务
- 检查防火墙设置，确保端口已开放
- 确认服务已成功启动
- 检查 `HOST` 配置（应设置为 `0.0.0.0` 以允许外部访问）

### 3. API调用失败
- 检查 `.env` 文件中的 `OPENAI_API_KEY` 是否正确
- 检查网络连接
- 查看服务日志了解详细错误信息

### 4. 依赖安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像（可选）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 十、完整运行流程总结

```bash
# 1. 进入项目目录
cd "C:\Users\Administrator\agent比赛"

# 2. 创建虚拟环境（可选但推荐）
python -m venv venv
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
# 创建 .env 文件并填入配置

# 5. 启动服务
python run_server.py

# 6. 测试服务（新开一个终端）
python test_api.py
# 或访问 http://localhost:8000/docs
```

## 十一、生产环境部署建议

1. **使用进程管理器**：如 `supervisor`、`pm2` 等
2. **配置反向代理**：如 Nginx
3. **启用HTTPS**：使用 SSL 证书
4. **日志管理**：配置日志轮转
5. **监控告警**：设置健康检查和监控

## 十二、开发模式

如果需要开发调试，可以使用热重载：

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

这样修改代码后会自动重启服务。