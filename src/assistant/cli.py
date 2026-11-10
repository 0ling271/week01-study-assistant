"""命令行入口：ask 子命令负责提问并保存笔记。"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .client import ask, save_note


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="assistant",
        description="AI 学习助手：提问、回答并自动生成学习笔记",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ask_parser = subparsers.add_parser("ask", help="提出一个问题")
    ask_parser.add_argument("question", help="要问的问题")
    ask_parser.add_argument("--model", default=None, help="覆盖默认模型名")
    ask_parser.add_argument(
        "--notes-dir",
        default="notes",
        help="笔记保存目录，默认 notes",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "ask":
        try:
            answer = ask(args.question, model=args.model)
        except RuntimeError as exc:
            # 配置类错误给干净提示，不抛堆栈
            parser.exit(1, f"错误：{exc}\n")
        note_path = save_note(args.question, answer, args.notes_dir)
        print(answer)
        print(f"\n[已保存] {note_path}")
