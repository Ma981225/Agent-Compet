"""
租房需求匹配智能体 Web API 服务
"""
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from agent import RentalHouseAgent
from models.house import HouseInfo
from utils.logger import log_info, log_error, log_warning
import time

app = FastAPI(title="租房需求匹配智能体API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = RentalHouseAgent()

# 创建v1版本的路由
v1_router = APIRouter(prefix="/v1", tags=["v1"])


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """聊天响应模型"""
    reply: str
    session_id: Optional[str] = None


class ResetRequest(BaseModel):
    """重置请求模型"""
    session_id: Optional[str] = None


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str
    message: str


@app.on_event("startup")
async def startup_event():
    """服务启动事件"""
    log_info("=" * 50)
    log_info("租房需求匹配智能体API服务启动")
    log_info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """服务关闭事件"""
    log_info("=" * 50)
    log_info("租房需求匹配智能体API服务关闭")
    log_info("=" * 50)


@app.get("/", response_model=HealthResponse)
async def root():
    """根路径，返回服务信息"""
    log_info("收到根路径访问请求")
    return HealthResponse(status="ok", message="租房需求匹配智能体API服务运行中")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    log_info("收到健康检查请求")
    return HealthResponse(status="ok", message="服务正常")


@v1_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    处理用户聊天请求
    
    Args:
        request: 聊天请求，包含用户消息和会话ID
        
    Returns:
        聊天响应，包含助手回复和会话ID
    """
    start_time = time.time()
    session_id = request.session_id or "unknown"
    
    try:
        log_info("[Chat] 收到聊天请求 | Session: %s | 消息长度: %d", 
                 session_id, len(request.message))
        log_info("[Chat] 用户消息: %s", request.message[:200] if len(request.message) > 200 else request.message)
        
        reply = agent.process_user_input(request.message)
        
        elapsed_time = time.time() - start_time
        log_info("[Chat] 处理完成 | Session: %s | 耗时: %.2f秒 | 回复长度: %d", 
                 session_id, elapsed_time, len(reply))
        log_info("[Chat] 生成回复: %s", reply[:200] if len(reply) > 200 else reply)
        
        return ChatResponse(
            reply=reply,
            session_id=request.session_id
        )
    except Exception as e:
        elapsed_time = time.time() - start_time
        log_error("[Chat] 处理失败 | Session: %s | 耗时: %.2f秒 | 错误: %s", 
                  session_id, elapsed_time, str(e))
        raise HTTPException(status_code=500, detail=f"处理请求时发生错误: {str(e)}")


@v1_router.post("/reset")
async def reset(request: Optional[ResetRequest] = None):
    """
    重置对话状态
    
    Args:
        request: 重置请求，包含会话ID（可选）
        
    Returns:
        重置结果
    """
    session_id = request.session_id if request else "unknown"
    try:
        log_info("[Reset] 收到重置请求 | Session: %s", session_id)
        agent.reset()
        log_info("[Reset] 对话状态已重置 | Session: %s", session_id)
        return {"status": "ok", "message": "对话状态已重置"}
    except Exception as e:
        log_error("[Reset] 重置失败 | Session: %s | 错误: %s", session_id, str(e))
        raise HTTPException(status_code=500, detail=f"重置失败: {str(e)}")


# 注册v1路由
app.include_router(v1_router)

if __name__ == "__main__":
    import uvicorn
    from config import SERVER_HOST, SERVER_PORT
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)