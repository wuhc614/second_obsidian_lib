"""
路由：POST /api/dream_analysis
周公解梦 — 接收用户梦境信息，调用 DeepSeek 大模型生成解梦分析报告
"""

from fastapi import APIRouter
from openai import AsyncOpenAI

from app.config import settings
from app.schemas import DreamAnalysisRequest, ApiResponse
from app.prompts import DREAM_SYSTEM_PROMPT, build_dream_user_prompt

router = APIRouter()


@router.post(
    "/api/dream_analysis",
    response_model=ApiResponse,
    summary="周公解梦",
    description="提交梦境信息，返回AI生成的解梦分析报告。参数缺失将返回 code=400。",
)
async def dream_analysis(payload: DreamAnalysisRequest):
    """
    周公解梦接口

    流程：
    1. Pydantic 自动校验必填字段（缺失则 FastAPI 返回 422 → 已由异常处理器转为 400）
    2. 组装 System + User Prompt
    3. 通过 OpenAI 兼容客户端调用 DeepSeek 大模型
    4. 返回统一格式 JSON
    """

    # ---- 构建提示词 ----
    user_prompt = build_dream_user_prompt(
        dream_content=payload.dream_content,
        dream_time=payload.dream_time,
        gender=payload.gender,
        age=payload.age,
        job=payload.job,
        recent_status=payload.recent_status,
        focus=payload.focus,
    )

    # ---- 初始化 DeepSeek 客户端（OpenAI 兼容） ----
    client = AsyncOpenAI(
        api_key=settings.deepseek_api_key,
        base_url=settings.deepseek_base_url,
    )

    # ---- 调用大模型 ----
    completion = await client.chat.completions.create(
        model=settings.deepseek_model,
        messages=[
            {"role": "system", "content": DREAM_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )

    # ---- 提取返回文本 ----
    content = completion.choices[0].message.content or ""

    return ApiResponse(code=200, msg="success", data=content)
