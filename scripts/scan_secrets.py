#!/usr/bin/env python3
"""无依赖、保守的已提交凭据赋值扫描。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".gradle", "target", "build", "node_modules", ".idea"}
TEXT_SUFFIXES = {".java", ".kt", ".kts", ".xml", ".yml", ".yaml", ".properties", ".json", ".toml", ".env", ".sh", ".py"}
PATTERNS = (
    re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token)\b\s*[:=]\s*[\"']?(?!\$\{|<|your-|replace-|example|changeme|dummy|test)[^\s\"']{8,}"),
    re.compile(r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
findings = []
for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
        continue
    if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".env", ".env.local"}:
        continue
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        continue
    for line_no, line in enumerate(lines, start=1):
        if any(pattern.search(line) for pattern in PATTERNS):
            findings.append(f"{path.relative_to(ROOT)}:{line_no}")
if findings:
    print("失败：可能提交了凭据：", *findings, sep="\n", file=sys.stderr)
    raise SystemExit(1)
print("通过：未发现明显凭据赋值")
