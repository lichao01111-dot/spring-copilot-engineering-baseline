#!/usr/bin/env python3
"""显式导出聚合工程度量；未配置允许上传时绝不访问网络。"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

from metrics_report import aggregate, load_events

ROOT = Path(os.environ.get("BASELINE_METRICS_ROOT", Path(__file__).resolve().parents[1])).resolve()
CONFIG = ROOT / ".baseline/metrics/config.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="导出匿名工程度量")
    parser.add_argument("--output", type=Path, help="写入本地聚合 JSON 文件")
    parser.add_argument("--upload", action="store_true", help="上传到已明确配置的内部 HTTPS 端点")
    arguments = parser.parse_args()
    report = aggregate(load_events())
    payload = json.dumps(report, ensure_ascii=False).encode("utf-8")
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_bytes(payload + b"\n")
        print(f"已导出本地聚合报告：{arguments.output}")
    if not arguments.upload:
        if not arguments.output:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    endpoint = config.get("endpoint")
    if not config.get("allow_upload") or not isinstance(endpoint, str) or not endpoint.startswith("https://"):
        raise SystemExit("上传被拒绝：config.json 必须明确 allow_upload=true 且配置内部 HTTPS endpoint")
    headers = {"Content-Type": "application/json"}
    if token := os.environ.get("BASELINE_METRICS_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(endpoint, data=payload, headers=headers, method="POST")
    with urlopen(request, timeout=10) as response:
        if not 200 <= response.status < 300:
            raise SystemExit(f"上传失败：HTTP {response.status}")
    print("已上传聚合匿名度量报告")


if __name__ == "__main__":
    main()
