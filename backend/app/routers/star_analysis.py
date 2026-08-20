"""
路由：POST /api/star_analysis
星座星盘分析测算 — 接收用户出生信息，调用 DeepSeek 大模型生成分析报告
"""

from fastapi import APIRouter
from openai import AsyncOpenAI

from app.config import settings
from app.schemas import StarAnalysisRequest, ApiResponse
from app.prompts import STAR_SYSTEM_PROMPT, build_star_user_prompt

router = APIRouter()


@router.post(
    "/api/star_analysis",
    response_model=ApiResponse,
    summary="星座星盘分析测算",
    description="提交出生信息，返回AI生成的星盘分析报告。参数缺失将返回 code=400。",
)
async def star_analysis(payload: StarAnalysisRequest):
    """
    星座星盘分析接口

    流程：
    1. Pydantic 自动校验必填字段（缺失则 FastAPI 返回 422 → 已由异常处理器转为 400）
    2. 组装 System + User Prompt
    3. 通过 OpenAI 兼容客户端调用 DeepSeek 大模型
    4. 返回统一格式 JSON
    """

    # ---- 构建提示词 ----
    user_prompt = build_star_user_prompt(
        birth_date=payload.birth_date,
        birth_time=payload.birth_time,
        birth_place=payload.birth_place,
        gender=payload.gender,
        emotion_status=payload.emotion_status,
        job=payload.job,
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
            {"role": "system", "content": STAR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )

    # ---- 提取返回文本 ----
    content = completion.choices[0].message.content or ""

    return ApiResponse(code=200, msg="success", data=content)
