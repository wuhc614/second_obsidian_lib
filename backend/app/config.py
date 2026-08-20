"""
应用配置模块
手动解析 .env 文件，不依赖 pydantic-settings 的 env_file（uvicorn子进程兼容性）
"""

import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings

_BACKEND_ROOT = Path(__file__).resolve().parent.parent


def _load_env_file() -> None:
    """手动解析 backend/.env 并注入 os.environ"""
    env_path = _BACKEND_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and val:
            os.environ[key] = val


# 模块导入时立即执行
_load_env_file()


class Settings(BaseSettings):
    """全局配置，从 os.environ 读取（已由 _load_env_file 注入）"""

    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"
    server_port: int = 8000
    frontend_origin: str = "http://localhost:5173"
    max_tokens: int = 800
    temperature: float = 0.5

    model_config = {"extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
