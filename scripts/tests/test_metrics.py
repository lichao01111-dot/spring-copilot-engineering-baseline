#!/usr/bin/env python3
"""度量采集必须拒绝自由文本，并只聚合允许字段。"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


BASELINE_ROOT = Path(__file__).resolve().parents[2]
RECORDER = BASELINE_ROOT / "scripts/record_metric.py"
REPORTER = BASELINE_ROOT / "scripts/metrics_report.py"


class MetricsTest(unittest.TestCase):
    def initialize_root(self, root: Path) -> None:
        config = root / ".baseline/metrics/config.json"
        config.parent.mkdir(parents=True)
        config.write_text(json.dumps({"schema_version": 1, "enabled": True, "project_key": "sample-project", "retention_days": 90, "allow_upload": False, "endpoint": None}), encoding="utf-8")

    def run_script(self, script: Path, root: Path, arguments: list[str], stdin: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *arguments],
            input=stdin,
            capture_output=True,
            text=True,
            check=False,
            env=os.environ | {"BASELINE_METRICS_ROOT": str(root)},
        )

    def test_recorder_writes_safe_event_and_report_aggregates_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize_root(root)
            event = '{"event_type":"guide_run","name":"spring-builder","outcome":"passed","duration_ms":1200}'
            record = self.run_script(RECORDER, root, ["--stdin"], event)
            report = self.run_script(REPORTER, root, ["--format", "json"])
            self.assertEqual(0, record.returncode, record.stderr)
            self.assertEqual(0, report.returncode, report.stderr)
            payload = json.loads(report.stdout)
            self.assertEqual(1, payload["event_count"])
            self.assertEqual(1, payload["by_name"]["spring-builder"]["count"])

    def test_recorder_rejects_free_text_and_identifier_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize_root(root)
            unsafe = '{"event_type":"guide_run","name":"spring-builder","outcome":"failed","prompt":"please fix customer 42"}'
            result = self.run_script(RECORDER, root, ["--stdin"], unsafe)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("不允许的度量字段", result.stderr)


if __name__ == "__main__":
    unittest.main()
