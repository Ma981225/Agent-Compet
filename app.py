"""
租房需求匹配智能体 Web API 服务
"""
from fastapi import FastAPI, HTTPException, APIRouter, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求验证错误"""
    log_error("[Validation] 请求验证失败 | Path: %s | Errors: %s", request.url.path, exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": str(request.body()) if hasattr(request, 'body') else None
        }
    )

agent = RentalHouseAgent()

# 创建v1版本的路由，添加/api前缀
v1_router = APIRouter(prefix="/api/v1", tags=["v1"])


class ChatRequest(BaseModel):
    """聊天请求模型（判题器格式）"""
    model_ip: str  # 判题器下发的模型服务IP
    session_id: str  # 会话ID（请求体中）
    message: str  # 用户消息


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
async def chat(
    request: ChatRequest,
    session_id: Optional[str] = Header(None, alias="Session-ID", description="会话ID，由评测接口生成")
):
    """
    处理用户聊天请求（判题器接口）
    
    Args:
        request: 聊天请求，包含model_ip、session_id、message
        session_id: 从请求头获取的Session-ID（可选，优先使用请求头，其次使用请求体中的session_id）
        
    Returns:
        聊天响应，包含助手回复和会话ID
    """
    from fastapi import Request
    from fastapi.exceptions import RequestValidationError
    
    start_time = time.time()
    
    # 优先使用请求头中的Session-ID，其次使用请求体中的session_id
    final_session_id = session_id or request.session_id or "unknown"
    
    try:
        log_info("[Chat] 收到判题器请求")
        log_info("[Chat] Model IP: %s | Session (Header): %s | Session (Body): %s | 消息长度: %d", 
                 request.model_ip, session_id, request.session_id, len(request.message))
        log_info("[Chat] 用户消息: %s", request.message[:200] if len(request.message) > 200 else request.message)
        
        # 传递model_ip和session_id给agent
        reply = agent.process_user_input(
            request.message, 
            model_ip=request.model_ip,
            session_id=final_session_id
        )
        
        elapsed_time = time.time() - start_time
        log_info("[Chat] 处理完成 | Session: %s | 耗时: %.2f秒 | 回复长度: %d", 
                 final_session_id, elapsed_time, len(reply))
        log_info("[Chat] 生成回复: %s", reply[:200] if len(reply) > 200 else reply)
        
        return ChatResponse(
            reply=reply,
            session_id=final_session_id
        )
    except RequestValidationError as e:
        log_error("[Chat] 请求验证失败: %s", str(e))
        log_error("[Chat] 错误详情: %s", e.errors() if hasattr(e, 'errors') else '')
        raise HTTPException(status_code=422, detail={"message": "请求验证失败", "errors": e.errors() if hasattr(e, 'errors') else str(e)})
    except Exception as e:
        elapsed_time = time.time() - start_time
        log_error("[Chat] 处理失败 | Session: %s | 耗时: %.2f秒 | 错误: %s", 
                  final_session_id, elapsed_time, str(e))
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


# 注册v1路由（必须在所有路由定义之后）
app.include_router(v1_router)


@app.on_event("startup")
async def startup_event():
    """服务启动事件"""
    from config import OPENAI_API_KEY
    
    log_info("=" * 50)
    log_info("租房需求匹配智能体API服务启动")
    log_info("=" * 50)
    
    # 检查配置
    if not OPENAI_API_KEY:
        log_warning("⚠️  OPENAI_API_KEY 未配置！")
        log_warning("请在.env文件中设置OPENAI_API_KEY，否则无法使用需求提取功能")
    else:
        masked_key = OPENAI_API_KEY[:8] + "..." + OPENAI_API_KEY[-4:] if len(OPENAI_API_KEY) > 12 else "***"
        log_info("✓ OpenAI API密钥已配置: %s", masked_key)
    
    # 打印所有注册的路由
    log_info("已注册的路由:")
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            methods = ", ".join(route.methods) if route.methods else "GET"
            log_info("  %s %s", methods, route.path)
        elif hasattr(route, "path"):
            log_info("  %s", route.path)


@app.on_event("shutdown")
async def shutdown_event():
    """服务关闭事件"""
    log_info("=" * 50)
    log_info("租房需求匹配智能体API服务关闭")
    log_info("=" * 50)

if __name__ == "__main__":
    import uvicorn
    from config import SERVER_HOST, SERVER_PORT
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)