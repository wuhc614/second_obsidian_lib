"""
Pydantic 数据模型 — 请求体校验 & 统一响应
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


# ============================================================
# 请求体模型
# ============================================================

class StarAnalysisRequest(BaseModel):
    """星座星盘分析 — 请求参数"""
    birth_date: str = Field(
        ...,
        min_length=1,
        description="出生年月日（如：1995-03-20）",
        examples=["1995-03-20"],
    )
    birth_time: str = Field(
        ...,
        min_length=1,
        description="出生时间（如：14:30）",
        examples=["14:30"],
    )
    birth_place: str = Field(
        ...,
        min_length=1,
        description="出生地点（如：广东省广州市）",
        examples=["广东省广州市"],
    )
    gender: str = Field(
        ...,
        min_length=1,
        description="性别（male / female / other 对应前端选项值）",
        examples=["male"],
    )
    emotion_status: str = Field(
        ...,
        min_length=1,
        description="情感状态（single / dating / married / complicated / secret）",
        examples=["single"],
    )
    job: str = Field(
        ...,
        min_length=1,
        description="职业身份",
        examples=["软件工程师"],
    )
    focus: str = Field(
        ...,
        min_length=1,
        description="测算关注点",
        examples=["事业方向与财运走势"],
    )


class DreamAnalysisRequest(BaseModel):
    """周公解梦 — 请求参数"""
    dream_content: str = Field(
        ...,
        min_length=1,
        description="梦境内容描述",
        examples=["梦见自己在一片无边无际的星空中飞翔..."],
    )
    dream_time: str = Field(
        ...,
        min_length=1,
        description="做梦时间（如：2025-06-15）",
        examples=["2025-06-15"],
    )
    gender: str = Field(
        ...,
        min_length=1,
        description="性别（male / female / other）",
        examples=["male"],
    )
    age: int = Field(
        ...,
        ge=1,
        le=120,
        description="年龄",
        examples=[28],
    )
    job: str = Field(
        ...,
        min_length=1,
        description="职业",
        examples=["设计师"],
    )
    recent_status: str = Field(
        ...,
        min_length=1,
        description="近期状态",
        examples=["压力较大"],
    )
    focus: str = Field(
        ...,
        min_length=1,
        description="解梦关注点",
        examples=["情感暗示与事业预兆"],
    )


# ============================================================
# 统一响应体模型
# ============================================================

class ApiResponse(BaseModel):
    """统一 API 响应格式"""
    code: int = 200
    msg: str = "success"
    data: Optional[Any] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 200,
                    "msg": "success",
                    "data": "这是大模型返回的分析结果文本...",
                }
            ]
        }
    }
