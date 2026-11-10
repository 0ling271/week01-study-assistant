# week01-study-assistant

AI 学习计划第 1 周项目：一个命令行 AI 学习助手，提问后自动回答，并把每次问答保存成 markdown 学习笔记。

## 功能

- 命令行提问，调用 OpenAI 兼容的大模型接口
- 自动把问答写入 `notes/` 目录，文件名带时间戳
- 密钥、网关、模型全部走环境变量，不写死在代码里
- 含 3 个单元测试（正常问答、密钥缺失、文件落盘）

## 快速开始

```bash
# 1. 克隆并进入仓库
git clone https://github.com/0ling271/week01-study-assistant.git
cd week01-study-assistant

# 2. 创建虚拟环境（Python 3.12，uv 会自动下载）
uv venv --python 3.12

# 3. 安装依赖
uv sync

# 4. 配置环境变量（PowerShell；密钥换成你自己的）
$env:LLM_API_KEY = "sk-你的密钥"
$env:LLM_MODEL = "你的模型名"
# 用非官方 OpenAI 平台时再加网关地址：
# $env:LLM_BASE_URL = "https://你的平台网关/v1"

# 5. 提问
uv run assistant ask "什么是注意力机制"
```

运行后会打印回答，并在 `notes/` 下生成一个 markdown 文件。

## 环境变量

| 变量 | 必填 | 说明 |
|---|---|---|
| `LLM_API_KEY` | 是 | 平台密钥 |
| `LLM_MODEL` | 否 | 模型 ID；不设置时用内置默认 |
| `LLM_BASE_URL` | 否 | OpenAI 兼容网关地址；官方 OpenAI 不用设 |

## 项目结构

```
src/assistant/
├─ client.py      # 模型调用与笔记落盘
├─ cli.py         # 命令行参数解析
└─ __main__.py    # python -m assistant 入口
tests/
└─ test_assistant.py
```

## 测试与检查

```bash
uv run pytest -q       # 单元测试
uv run ruff check .    # 代码风格检查
```
