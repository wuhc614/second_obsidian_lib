"""
星梦智能助手 — FastAPI 应用入口
提供跨域支持、统一异常处理、路由注册
"""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.schemas import ApiResponse
from app.routers import star_analysis, dream_analysis


# ============================================================
# 统一响应格式中间件
# 拦截所有 422 及其他异常响应，转换为统一 JSON 格式
# ============================================================

class UnifyResponseMiddleware(BaseHTTPMiddleware):
    """
    统一响应格式中间件
    - 拦截 422 响应（Pydantic校验失败由FastAPI内部转为422响应，不会抛给中间件）
    - 将其转换为 HTTP 200 + code=400 的统一格式
    - 兜底 500 异常
    """

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            # FastAPI 内部已将 RequestValidationError 转为 422 响应
            # 我们检查响应对象的 status_code 进行转换
            if response.status_code == 422:
                # 读取原始422响应体，提取第一个字段错误
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                import json
                try:
                    errors = json.loads(body).get("detail", [])
                except (json.JSONDecodeError, AttributeError):
                    errors = []

                detail = "参数校验失败"
                if errors and isinstance(errors, list) and len(errors) > 0:
                    first = errors[0]
                    field = first.get("loc", ["unknown"])[-1]
                    msg = first.get("msg", "invalid")
                    detail = f"参数 [{field}] {msg}"

                return JSONResponse(
                    status_code=200,
                    content=ApiResponse(code=400, msg=detail, data=None).model_dump(),
                )
            return response
        except Exception as exc:
            import traceback
            traceback.print_exc()
            return JSONResponse(
                status_code=200,
                content=ApiResponse(code=500, msg=f"服务器内部错误: {str(exc)}", data=None).model_dump(),
            )


# ============================================================
# 应用生命周期
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动 / 关闭时打印运行信息"""
    print(">>> 星梦智能助手后端启动中...")
    print(f"    DeepSeek API: {settings.deepseek_base_url}")
    print(f"    Model: {settings.deepseek_model}")
    if not settings.deepseek_api_key:
        print("    [WARN] DEEPSEEK_API_KEY 未配置，请在 .env 中填入密钥")
    else:
        print(f"    [OK] API Key 已配置 ({settings.deepseek_api_key[:8]}***)")
    print(f"    CORS 白名单: {settings.frontend_origin}")
    yield
    print(">>> 服务已关闭")


# ---- 创建 FastAPI 实例 ----
app = FastAPI(
    title="星梦智能助手 API",
    description="星座星盘分析 & 周公解梦 — DeepSeek 大模型驱动",
    version="1.0.0",
    lifespan=lifespan,
)

# ============================================================
# CORS 跨域配置
# ============================================================

origins = [
    origin.strip()
    for origin in settings.frontend_origin.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 统一响应中间件：在 CORS 之后注册，确保 CORS 头优先
app.add_middleware(UnifyResponseMiddleware)

# ============================================================
# 注册路由
# ============================================================

app.include_router(star_analysis.router, tags=["星座星盘"])
app.include_router(dream_analysis.router, tags=["周公解梦"])

# ============================================================
# 健康检查接口
# ============================================================

@app.get("/api/health", response_model=ApiResponse, tags=["系统"])
async def health_check():
    """服务健康检查"""
    import os
    env_key = os.getenv("DEEPSEEK_API_KEY", "")
    settings_key = settings.deepseek_api_key
    return ApiResponse(
        code=200,
        msg="success",
        data={
            "status": "running",
            "version": "1.0.0",
            "deepseek_configured": bool(settings_key),
            "key_source": "env" if env_key else "settings" if settings_key else "none",
        },
    )


# ============================================================
# 直接运行入口
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.server_port,
        reload=True,
    )
