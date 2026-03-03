"""
启动Web API服务
"""
import uvicorn
from config import SERVER_HOST, SERVER_PORT

if __name__ == "__main__":
    print("正在启动租房需求匹配智能体API服务...")
    print(f"服务地址: http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"API文档: http://{SERVER_HOST}:{SERVER_PORT}/docs")
    print(f"健康检查: http://{SERVER_HOST}:{SERVER_PORT}/health")
    print(f"Swagger UI: http://{SERVER_HOST}:{SERVER_PORT}/docs")
    print(f"ReDoc: http://{SERVER_HOST}:{SERVER_PORT}/redoc")
    print("\n按 Ctrl+C 停止服务\n")
    
    uvicorn.run(
        "app:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=False,
        log_level="info"
    )