#!/usr/bin/env python3
"""报告常见 Java 性能风险；PERFORMANCE_RISK_MODE=strict 时阻断未批准用法。"""
from pathlib import Path
import os
import re
import sys

ROOT = Path(os.environ.get("BASELINE_SCAN_ROOT", Path(__file__).resolve().parents[1])).resolve()
MODE = os.environ.get("PERFORMANCE_RISK_MODE", "warn").lower()
SKIP_PARTS = {".git", "target", "build", ".gradle", "node_modules"}
SOURCE_SUFFIXES = {".java", ".kt", ".kts"}
RULES = {
    "PERF-UNBOUNDED-FIND-ALL": re.compile(r"\.findAll\s*\(\s*\)"),
    "PERF-PARALLEL-STREAM": re.compile(r"\.parallelStream\s*\("),
    "PERF-THREAD-SLEEP": re.compile(r"Thread\.sleep\s*\("),
    "PERF-MANUAL-THREAD": re.compile(r"new\s+Thread\s*\(|Executors\.new(?:Fixed|Cached|Single)ThreadPool"),
    "PERF-DEFAULT-ASYNC": re.compile(r"@Async(?:\s|$|\()"),
}
ALLOW_PREFIX = re.compile(r"baseline-risk-allow:\s*(PERF-[A-Z-]+)\s+([A-Z]+-\d+)")

def allowed(rule: str, lines: list[str], index: int) -> bool:
    return any((match := ALLOW_PREFIX.search(line)) and match.group(1) == rule for line in lines[max(0, index - 1):index + 1])

findings: list[str] = []
for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in SKIP_PARTS for part in path.parts) or path.suffix not in SOURCE_SUFFIXES:
        continue
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        continue
    for index, line in enumerate(lines):
        for rule, pattern in RULES.items():
            if pattern.search(line) and not allowed(rule, lines, index):
                findings.append(f"{path.relative_to(ROOT)}:{index + 1} [{rule}]")

if findings:
    stream = sys.stderr if MODE == "strict" else sys.stdout
    print("性能风险需要评估：", *findings, sep="\n", file=stream)
    print("需要保留时，在同一行或前一行添加 baseline-risk-allow 和工单号，并完成性能评估。", file=stream)
    if MODE == "strict":
        raise SystemExit(1)
    print("警告模式：未阻断。CI 推荐设置 PERFORMANCE_RISK_MODE=strict。")
else:
    print("通过：未发现需评估的 Java 性能风险")
