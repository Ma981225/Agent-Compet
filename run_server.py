"""
启动Web API服务
"""
import uvicorn
from config import SERVER_HOST, SERVER_PORT
from utils.logger import log_info

if __name__ == "__main__":
    import socket
    
    log_info("=" * 60)
    log_info("正在启动租房需求匹配智能体API服务...")
    
    # 获取本机IP地址
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "localhost"
    
    log_info("服务配置 - Host: %s, Port: %d", SERVER_HOST, SERVER_PORT)
    log_info("服务地址:")
    log_info("  本地访问: http://127.0.0.1:%d", SERVER_PORT)
    log_info("  本机IP:   http://%s:%d", local_ip, SERVER_PORT)
    log_info("  外部访问: http://<你的公网IP>:%d", SERVER_PORT)
    log_info("API端点:")
    log_info("  聊天接口: POST http://%s:%d/v1/chat", local_ip, SERVER_PORT)
    log_info("  重置接口: POST http://%s:%d/v1/reset", local_ip, SERVER_PORT)
    log_info("  健康检查: GET  http://%s:%d/health", local_ip, SERVER_PORT)
    log_info("  API文档:  http://%s:%d/docs", local_ip, SERVER_PORT)
    log_info("=" * 60)
    log_info("按 Ctrl+C 停止服务")
    log_info("")
    
    uvicorn.run(
        "app:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=False,
        log_level="info"
    )