#!/usr/bin/env python3
"""结构校验必须拒绝缺少 orchestrator 状态机的基线。"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


BASELINE_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = BASELINE_ROOT / "scripts/validate_baseline.py"


class BaselineValidationTest(unittest.TestCase):
    def test_validator_rejects_missing_orchestrator_state_machine(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "baseline"
            shutil.copytree(BASELINE_ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__", "events.jsonl", "reports", "exports"))
            orchestrator = target / ".github/agents/spring-orchestrator.agent.md"
            orchestrator.write_text(orchestrator.read_text(encoding="utf-8").replace("## 任务状态机", "## 状态说明"), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR)],
                capture_output=True,
                text=True,
                check=False,
                env=os.environ | {"BASELINE_ROOT": str(target)},
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("spring-orchestrator 缺少任务状态机标记", result.stderr)

    def test_validator_rejects_workspace_map_without_service_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "baseline"
            shutil.copytree(BASELINE_ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__", "events.jsonl", "reports", "exports"))
            (target / "workspace-map.md").write_text(
                "| 服务 | 修改前必须阅读 |\n"
                "|---|---|\n"
                "| order-service | `services/order-service/SERVICE.md` |\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(VALIDATOR)],
                capture_output=True,
                text=True,
                check=False,
                env=os.environ | {"BASELINE_ROOT": str(target)},
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("workspace-map.md 引用的服务上下文不存在", result.stderr)


if __name__ == "__main__":
    unittest.main()
