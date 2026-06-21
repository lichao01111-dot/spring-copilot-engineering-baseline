#!/usr/bin/env python3
"""阻断未明确批准的高风险 Java 安全用法。不能替代 SAST 或人工威胁建模。"""
from pathlib import Path
import os
import re
import sys

ROOT = Path(os.environ.get("BASELINE_SCAN_ROOT", Path(__file__).resolve().parents[1])).resolve()
SKIP_PARTS = {".git", "target", "build", ".gradle", "node_modules"}
SOURCE_SUFFIXES = {".java", ".kt", ".kts"}
RULES = {
    "SEC-CMD-EXEC": re.compile(r"Runtime\.getRuntime\(\)\.exec\s*\(|new\s+ProcessBuilder\s*\("),
    "SEC-JAVA-SERIALIZATION": re.compile(r"new\s+ObjectInputStream\s*\("),
    "SEC-TRUST-ALL-TLS": re.compile(r"X509TrustManager|NoopHostnameVerifier|trustAllCertificates|TrustAll"),
    "SEC-CORS-WILDCARD": re.compile(r"@CrossOrigin\s*\(\s*[\"']\*[\"']\s*\)|allowedOrigins\s*\(\s*[\"']\*[\"']"),
    "SEC-CSRF-DISABLED": re.compile(r"csrf\s*\([^)]*disable\s*\(|csrf\s*\(\s*\)\s*\.disable\s*\("),
    "SEC-NATIVE-SQL-CONCAT": re.compile(r"(?:createNativeQuery|jdbcTemplate\.(?:query|update|execute))\s*\([^\n]*\+"),
}
ALLOW_PREFIX = re.compile(r"baseline-risk-allow:\s*(SEC-[A-Z-]+)\s+([A-Z]+-\d+)")

def allowed(rule: str, lines: list[str], index: int) -> bool:
    candidates = lines[max(0, index - 1):index + 1]
    return any((match := ALLOW_PREFIX.search(line)) and match.group(1) == rule for line in candidates)

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
    print("失败：发现未经批准的高风险安全用法：", *findings, sep="\n", file=sys.stderr)
    print("如确有必要，需在同一行或前一行添加：// baseline-risk-allow: <规则编号> <工单号>，并完成安全评估。", file=sys.stderr)
    raise SystemExit(1)
print("通过：未发现未经批准的高风险 Java 安全用法")
