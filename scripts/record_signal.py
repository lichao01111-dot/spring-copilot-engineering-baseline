#!/usr/bin/env python3
"""从标准输入追加一个隐私安全的结构化演进信号。"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ALLOWED = {"skill", "version", "outcome", "reason_code", "check_results", "human_override", "task_kind"}
REQUIRED = {"skill", "outcome", "reason_code"}
payload = json.load(sys.stdin)
if not isinstance(payload, dict) or not REQUIRED.issubset(payload): raise SystemExit("信号必须包含 skill、outcome 和 reason_code")
if set(payload) - ALLOWED: raise SystemExit("信号包含不支持字段；不允许自由文本或原始数据")
if not all(isinstance(payload[key], str) and payload[key] for key in REQUIRED): raise SystemExit("skill、outcome 和 reason_code 必须为非空字符串")
payload["timestamp"] = datetime.now(timezone.utc).isoformat()
target = Path(__file__).resolve().parents[1] / ".baseline/evolution/signals.jsonl"
with target.open("a", encoding="utf-8") as stream: stream.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
