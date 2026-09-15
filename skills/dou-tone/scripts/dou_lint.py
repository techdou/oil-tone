#!/usr/bin/env python3
"""Deterministic lint checks for dou-tone Chinese writing."""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

Rule = tuple[re.Pattern[str], str]

FAIL_RULES: tuple[Rule, ...] = (
    (re.compile(r"(?:搞|弄)(?:顺|清楚|明白|好|完|懂|定|起来|下去)"), "改用能够说明真实动作和结果的准确动词。"),
    (re.compile(r"承接(?:需求|任务|工作|内容)"), "说明具体是处理、实现、负责还是接收。"),
    (re.compile(r"(?:吃下|吞下).{0,10}(?:对话|内容|信息|上下文)"), "改用读取、接收、包含等准确动词。"),
    (re.compile(r"(?:把)?(?:内容|信息|上下文).{0,8}(?:塞进|塞到|喂给)"), "改用写入、添加、提供等准确动词。"),
    (re.compile(r"跑测试"), "使用“运行测试”。"),
    (re.compile(r"(?:赋能|撬动|抓手|沉淀价值|价值落地)"), "删除宣传黑话，说明具体作用。"),
    (re.compile(r"原因很简单[：:，,。]?"), "删除模板化领起语，直接说明原因。"),
    (re.compile(r"(?:真正重要的是|真正的关键是|从更大的角度看)"), "删除没有增加信息的升华表达。"),
    (re.compile(r"(?:当然可以|希望这对(?:你|您)有帮助|如需更多(?:信息|帮助))"), "删除成稿中的聊天残留。"),
)

WARN_RULES: tuple[Rule, ...] = (
    (re.compile(r"(?:在当今|在当前).{0,18}(?:时代|背景|环境)下"), "确认背景是否提供必要信息。"),
    (re.compile(r"随着.{0,18}(?:不断|持续)(?:发展|演变|变化)"), "确认变化是否与后文存在具体关系。"),
    (re.compile(r"(?:值得注意的是|需要指出的是|毋庸置疑|不可否认的是?)"), "确认领起语是否承担真实限定或转折。"),
    (re.compile(r"(?:标志着|代表着).{0,24}(?:重要|关键)(?:一步|时刻|转折点)"), "改为材料已经确认的动作、变化或结果。"),
    (re.compile(r"为.{1,24}奠定(?:了)?(?:坚实的?)?基础"), "说明具体产生了什么后续条件或结果。"),
    (re.compile(r"(?:彰显|凸显|体现)(?:了)?.{0,20}(?:重要性|意义|价值)"), "确认重要性判断是否有材料支持。"),
    (re.compile(r"(?:业内|行业|专家|观察者)(?:普遍)?(?:认为|指出|表示)"), "给出明确来源；没有来源时删除模糊归因。"),
    (re.compile(r"(?:很多|不少|部分)用户(?:认为|指出|表示|反馈)"), "确认用户反馈是否有明确材料依据。"),
    (re.compile(r"(?:有|相关|多项|大量)研究(?:均)?(?:表明|显示|指出)"), "学术文本需要明确来源；其他文本避免模糊权威背书。"),
    (re.compile(r"(?:未来可期|开启(?:了)?(?:全新|新的?)篇章)"), "删除通用乐观结尾，改写为具体结果或安排。"),
    (re.compile(r"(?:可能|或许|也许|在一定程度上|在某种程度上).{0,8}(?:可能|或许|也许|在一定程度上|在某种程度上)"), "合并重复限定。"),
)


def visible_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_fence = False
    for number, raw in enumerate(text.splitlines(), start=1):
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        clean = re.sub(r"<[^>]+>", " ", raw)
        clean = re.sub(r"`[^`]*`", " ", clean)
        clean = html.unescape(re.sub(r"\s+", " ", clean)).strip()
        if clean:
            lines.append((number, clean))
    return lines


def scan(text: str, rules: tuple[Rule, ...]) -> list[tuple[int, str, str]]:
    out = []
    for line_no, line in visible_lines(text):
        for pattern, message in rules:
            if pattern.search(line):
                out.append((line_no, line, message))
    return out


def self_test() -> int:
    bad = "先把流程搞顺。\n这套方案可以赋能团队。\n真正重要的是，我们理解了边界。"
    warn = "随着人工智能技术的不断发展，工具越来越多。\n有研究表明，这种方法有效。"
    good = "检查流程中的调用关系并修正错误。\n该功能用于批量处理文件。"
    ok = len(scan(bad, FAIL_RULES)) == 3 and len(scan(warn, WARN_RULES)) == 2 and not scan(good, FAIL_RULES) and not scan(good, WARN_RULES)
    print("PASS  dou-tone lint self-test" if ok else "FAIL  dou-tone lint self-test")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Check text for known dou-tone writing issues.")
    parser.add_argument("files", nargs="*")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.files:
        parser.error("provide one or more UTF-8 files, or use --self-test")
    failed = False
    warned = False
    for name in args.files:
        text = sys.stdin.read() if name == "-" else Path(name).read_text(encoding="utf-8")
        for line_no, line, message in scan(text, FAIL_RULES):
            print(f"FAIL  {name}:{line_no}: {line}\n      {message}")
            failed = True
        for line_no, line, message in scan(text, WARN_RULES):
            print(f"WARN  {name}:{line_no}: {line}\n      {message}")
            warned = True
    if not failed and not warned:
        print("PASS  no known dou-tone issues")
    elif not failed:
        print("PASS  no confirmed failures; review warnings")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
