#!/usr/bin/env python3
"""追加隐私安全工程度量事件；默认只写入本地 JSONL。"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(os.environ.get("BASELINE_METRICS_ROOT", Path(__file__).resolve().parents[1])).resolve()
CONFIG_PATH = ROOT / ".baseline/metrics/config.json"
TARGET = ROOT / ".baseline/metrics/events.jsonl"
EVENT_TYPES = {"guide_run", "agent_review", "check_run", "risk_scan", "release_assessment", "evolution_proposal"}
OUTCOMES = {"passed", "failed", "blocked", "warn", "skipped"}
SEVERITIES = {"P0", "P1", "P2"}
ENVIRONMENTS = {"local", "ci"}
IDENTIFIER = re.compile(r"^[a-zA-Z0-9_.-]{1,100}$")
REASON = re.compile(r"^[A-Z0-9_]{1,100}$")


def load_config() -> dict[str, object]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def parse_input(arguments: argparse.Namespace) -> dict[str, object]:
    if arguments.stdin:
        value = json.load(sys.stdin)
        if not isinstance(value, dict):
            raise ValueError("标准输入必须是 JSON 对象")
        return value
    return {key: value for key, value in {
        "event_type": arguments.event_type,
        "name": arguments.name,
        "outcome": arguments.outcome,
        "duration_ms": arguments.duration_ms,
        "reason_code": arguments.reason_code,
        "severity": arguments.severity,
        "environment": arguments.environment,
    }.items() if value is not None}


def validate(event: dict[str, object], config: dict[str, object]) -> dict[str, object]:
    allowed = {"event_type", "name", "outcome", "duration_ms", "reason_code", "severity", "environment"}
    unknown = set(event) - allowed
    if unknown:
        raise ValueError(f"不允许的度量字段：{', '.join(sorted(unknown))}")
    if event.get("event_type") not in EVENT_TYPES:
        raise ValueError("event_type 无效")
    if event.get("outcome") not in OUTCOMES:
        raise ValueError("outcome 无效")
    if not isinstance(event.get("name"), str) or not IDENTIFIER.fullmatch(event["name"]):
        raise ValueError("name 只能包含字母、数字、点、下划线和短横线")
    if "duration_ms" in event and (not isinstance(event["duration_ms"], int) or not 0 <= event["duration_ms"] <= 86400000):
        raise ValueError("duration_ms 必须在 0 到 86400000 之间")
    if "reason_code" in event and (not isinstance(event["reason_code"], str) or not REASON.fullmatch(event["reason_code"])):
        raise ValueError("reason_code 必须是大写枚举码")
    if "severity" in event and event["severity"] not in SEVERITIES:
        raise ValueError("severity 无效")
    environment = event.get("environment", "ci" if os.environ.get("CI") else "local")
    if environment not in ENVIRONMENTS:
        raise ValueError("environment 无效")
    project_key = config.get("project_key")
    if not isinstance(project_key, str) or not IDENTIFIER.fullmatch(project_key):
        raise ValueError("config.json 的 project_key 无效")
    return {
        "schema_version": 1,
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "project_key": project_key,
        **event,
        "environment": environment,
    }


def prune_expired_events(retention_days: object) -> None:
    if not TARGET.exists() or not isinstance(retention_days, int) or retention_days <= 0:
        return
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    retained: list[str] = []
    for line in TARGET.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
            occurred_at = datetime.fromisoformat(event["occurred_at"])
            if occurred_at >= cutoff:
                retained.append(line)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            retained.append(line)
    TARGET.write_text("\n".join(retained) + ("\n" if retained else ""), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="记录匿名工程度量事件")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取 JSON 对象")
    parser.add_argument("--event-type", choices=sorted(EVENT_TYPES))
    parser.add_argument("--name")
    parser.add_argument("--outcome", choices=sorted(OUTCOMES))
    parser.add_argument("--duration-ms", type=int)
    parser.add_argument("--reason-code")
    parser.add_argument("--severity", choices=sorted(SEVERITIES))
    parser.add_argument("--environment", choices=sorted(ENVIRONMENTS))
    arguments = parser.parse_args()
    config = load_config()
    if not config.get("enabled", True):
        print("度量采集已禁用")
        return
    event = validate(parse_input(arguments), config)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    prune_expired_events(config.get("retention_days"))
    with TARGET.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"已记录度量事件：{event['event_type']}/{event['name']}/{event['outcome']}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"度量事件被拒绝：{error}")
