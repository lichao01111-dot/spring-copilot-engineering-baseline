#!/usr/bin/env python3
"""行为测试：安全/性能风险扫描必须识别风险，并接受带工单的例外。"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


BASELINE_ROOT = Path(__file__).resolve().parents[2]
SECURITY = BASELINE_ROOT / "scripts/security_preflight.py"
PERFORMANCE = BASELINE_ROOT / "scripts/performance_preflight.py"


class PreflightTest(unittest.TestCase):
    def run_scan(self, script: Path, source: str, mode: str | None = None, relative_path: str = "src/main/java/RiskyCode.java") -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / relative_path
            source_path.parent.mkdir(parents=True)
            source_path.write_text(source, encoding="utf-8")
            environment = os.environ | {"BASELINE_SCAN_ROOT": str(root)}
            if mode:
                environment["PERFORMANCE_RISK_MODE"] = mode
            return subprocess.run(
                [sys.executable, str(script)],
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_security_scan_blocks_command_execution_without_approval(self) -> None:
        result = self.run_scan(SECURITY, "class RiskyCode { void run() throws Exception { Runtime.getRuntime().exec(\"id\"); } }")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("SEC-CMD-EXEC", result.stderr)

    def test_security_scan_accepts_reviewed_command_execution(self) -> None:
        result = self.run_scan(SECURITY, "// baseline-risk-allow: SEC-CMD-EXEC PLATFORM-123\nclass RiskyCode { void run() throws Exception { Runtime.getRuntime().exec(\"id\"); } }")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_performance_scan_warns_locally_and_blocks_in_strict_mode(self) -> None:
        source = "class RiskyCode { void run() { repository.findAll(); } }"
        warning = self.run_scan(PERFORMANCE, source)
        strict = self.run_scan(PERFORMANCE, source, "strict")
        self.assertEqual(0, warning.returncode)
        self.assertIn("PERF-UNBOUNDED-FIND-ALL", warning.stdout)
        self.assertNotEqual(0, strict.returncode)
        self.assertIn("PERF-UNBOUNDED-FIND-ALL", strict.stderr)

    def test_performance_scan_accepts_reviewed_exception_in_strict_mode(self) -> None:
        source = "// baseline-risk-allow: PERF-UNBOUNDED-FIND-ALL REPORT-238\nclass RiskyCode { void run() { repository.findAll(); } }"
        result = self.run_scan(PERFORMANCE, source, "strict")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_performance_scan_skips_test_source_directories(self) -> None:
        source = "class RiskyCode { void run() { repository.findAll(); Thread.sleep(10); } }"
        result = self.run_scan(PERFORMANCE, source, "strict", "src/test/java/RiskyCode.java")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("未发现需评估", result.stdout)


if __name__ == "__main__":
    unittest.main()
