"""学习助手的单元测试：用假客户端，不发起真实网络请求。"""

from __future__ import annotations

import pytest

from assistant.client import ask, build_client, save_note


class _FakeMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class _FakeChoice:
    def __init__(self, content: str) -> None:
        self.message = _FakeMessage(content)


class _FakeResponse:
    def __init__(self, content: str) -> None:
        self.choices = [_FakeChoice(content)]


class _FakeCompletions:
    def __init__(self, content: str) -> None:
        self._content = content
        self.last_kwargs: dict | None = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return _FakeResponse(self._content)


class _FakeChat:
    def __init__(self, content: str) -> None:
        self.completions = _FakeCompletions(content)


class _FakeClient:
    def __init__(self, content: str = "模拟回答") -> None:
        self.chat = _FakeChat(content)


def test_ask_returns_answer_and_passes_question():
    """正常问答：返回模型文本，且问题被放进 user 消息。"""
    fake = _FakeClient("这是答案")
    result = ask("什么是注意力机制", model="test-model", client=fake)

    assert result == "这是答案"
    kwargs = fake.chat.completions.last_kwargs
    assert kwargs["model"] == "test-model"
    messages = kwargs["messages"]
    assert messages[-1] == {"role": "user", "content": "什么是注意力机制"}


def test_build_client_raises_without_api_key(monkeypatch):
    """API 异常路径：缺少密钥时抛出明确错误，而不是报一堆网络错误。"""
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="LLM_API_KEY"):
        build_client()


def test_save_note_writes_markdown(tmp_path):
    """文件落盘：生成 md 文件，内容包含问题和回答。"""
    path = save_note("问题文本", "回答文本", notes_dir=tmp_path)

    assert path.exists()
    assert path.suffix == ".md"
    body = path.read_text(encoding="utf-8")
    assert "问题文本" in body
    assert "回答文本" in body
