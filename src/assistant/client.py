"""大模型客户端：封装一个 OpenAI 兼容的问答调用。"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from openai import OpenAI

SYSTEM_PROMPT = "你是一个学习助手，用简洁准确的中文回答技术问题。"
DEFAULT_MODEL = "gpt-4o-mini"


def build_client() -> OpenAI:
    """从环境变量构建客户端。

    LLM_API_KEY：必填，平台颁发的密钥
    LLM_BASE_URL：可选，兼容 OpenAI 协议的平台网关地址
    """
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise RuntimeError("未设置环境变量 LLM_API_KEY，请先配置后再运行")
    base_url = os.environ.get("LLM_BASE_URL")
    kwargs: dict[str, str] = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def ask(
    question: str,
    model: str | None = None,
    client: OpenAI | None = None,
) -> str:
    """向模型提问，返回回答文本。

    模型名的优先级：显式参数 > 环境变量 LLM_MODEL > 内置默认值。
    client 可注入，方便测试时替换成假对象。
    """
    active_client = client or build_client()
    active_model = model or os.environ.get("LLM_MODEL") or DEFAULT_MODEL
    response = active_client.chat.completions.create(
        model=active_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content


def save_note(
    question: str,
    answer: str,
    notes_dir: Path | str = "notes",
) -> Path:
    """把一次问答保存为 markdown 文件，返回文件路径。"""
    directory = Path(notes_dir)
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = directory / f"{timestamp}.md"
    path.write_text(
        f"# 问题\n\n{question}\n\n# 回答\n\n{answer}\n",
        encoding="utf-8",
    )
    return path
