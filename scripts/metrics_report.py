#!/usr/bin/env python3
"""将本地工程度量 JSONL 聚合为 JSON 或 Markdown 报告。"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import statistics
from typing import Any

ROOT = Path(os.environ.get("BASELINE_METRICS_ROOT", Path(__file__).resolve().parents[1])).resolve()
EVENTS = ROOT / ".baseline/metrics/events.jsonl"


def load_events() -> list[dict[str, Any]]:
    if not EVENTS.exists():
        return []
    items: list[dict[str, Any]] = []
    for line_number, line in enumerate(EVENTS.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"第 {line_number} 行不是对象")
        items.append(value)
    return items


def aggregate(events: list[dict[str, Any]]) -> dict[str, Any]:
    outcomes = Counter(str(event["outcome"]) for event in events)
    event_types = Counter(str(event["event_type"]) for event in events)
    project_keys = sorted({str(event["project_key"]) for event in events})
    names: dict[str, dict[str, Any]] = defaultdict(lambda: {"count": 0, "outcomes": Counter(), "durations": []})
    reasons = Counter()
    for event in events:
        bucket = names[str(event["name"])]
        bucket["count"] += 1
        bucket["outcomes"][str(event["outcome"])] += 1
        if isinstance(event.get("duration_ms"), int):
            bucket["durations"].append(event["duration_ms"])
        if event.get("reason_code"):
            reasons[str(event["reason_code"])] += 1
    by_name: dict[str, Any] = {}
    for name, bucket in sorted(names.items()):
        durations = bucket.pop("durations")
        by_name[name] = {
            "count": bucket["count"],
            "outcomes": dict(bucket["outcomes"]),
            "median_duration_ms": int(statistics.median(durations)) if durations else None,
        }
    return {
        "event_count": len(events),
        "project_keys": project_keys,
        "period_start": min((str(event["occurred_at"]) for event in events), default=None),
        "period_end": max((str(event["occurred_at"]) for event in events), default=None),
        "outcomes": dict(outcomes),
        "event_types": dict(event_types),
        "by_name": by_name,
        "top_reason_codes": [{"reason_code": code, "count": count} for code, count in reasons.most_common(10)],
    }


def render_markdown(report: dict[str, Any]) -> str:
    project_keys = ", ".join(report["project_keys"]) if report["project_keys"] else "无"
    lines = ["# 工程基线度量报告", "", f"- 项目别名：{project_keys}", f"- 事件数：{report['event_count']}", f"- 时间范围：{report['period_start'] or '无'} 至 {report['period_end'] or '无'}", "", "## 总体结果", "", "| 结果 | 数量 |", "|---|---:|"]
    lines.extend(f"| {outcome} | {count} |" for outcome, count in sorted(report["outcomes"].items()))
    lines.extend(["", "## 事件类型", "", "| 类型 | 数量 |", "|---|---:|"])
    lines.extend(f"| {event_type} | {count} |" for event_type, count in sorted(report["event_types"].items()))
    lines.extend(["", "## 按能力/检查汇总", "", "| 名称 | 次数 | 结果 | 中位耗时（ms） |", "|---|---:|---|---:|"])
    for name, value in report["by_name"].items():
        outcomes = ", ".join(f"{key}:{count}" for key, count in sorted(value["outcomes"].items()))
        lines.append(f"| {name} | {value['count']} | {outcomes} | {value['median_duration_ms'] if value['median_duration_ms'] is not None else '-'} |")
    lines.extend(["", "## 高频原因码", "", "| 原因码 | 次数 |", "|---|---:|"])
    lines.extend(f"| {item['reason_code']} | {item['count']} |" for item in report["top_reason_codes"])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="生成工程基线聚合报告")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    report = aggregate(load_events())
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if arguments.format == "json" else render_markdown(report)
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(content, encoding="utf-8")
        print(f"已生成报告：{arguments.output}")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
