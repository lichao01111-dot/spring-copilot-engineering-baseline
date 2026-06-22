#!/usr/bin/env python3
"""Spring Copilot 工程基线的无依赖结构校验。"""
from pathlib import Path
import json
import os
import sys

ROOT = Path(os.environ.get("BASELINE_ROOT", Path(__file__).resolve().parents[1])).resolve()
GUIDES = ["spring-discovery", "requirements-to-spec", "api-contract-builder", "spring-architecture", "dev-planner", "spring-builder", "database-migration", "bug-fixer", "code-review", "release-builder", "evolution-engine"]
REQUIRED_FILES = [
    ".github/copilot-instructions.md", ".github/CODEOWNERS.example",
    ".github/agents/spring-orchestrator.agent.md", ".github/agents/code-reviewer.agent.md", ".github/agents/evolution-runner.agent.md",
    ".github/instructions/java-spring.instructions.md", ".github/instructions/testing.instructions.md", ".github/instructions/database.instructions.md", ".github/instructions/security.instructions.md",
    ".baseline/project-profile.yaml", ".baseline/evolution/signals.jsonl", ".baseline/evolution/proposals.md", ".baseline/hooks/hooks.json", ".baseline/hooks/pre-commit", ".baseline/hooks/pre-push", ".baseline/hooks/check-review-required.sh", ".baseline/hooks/check-evolution-pending.sh",
    ".editorconfig", ".baseline/metrics/config.json", "templates/task-state.yaml", "templates/adr.md", "templates/review-report.md", "templates/goal.md", "templates/migration-plan.md", "templates/release-checklist.md", "templates/service-boundary.md", "templates/security-performance-assessment.md", "standards/service-boundary-and-deployment.md", "standards/java-readability-and-conventions.md", "standards/java-tooling-integration.md", "standards/security-and-performance-gates.md", "standards/metrics-and-privacy.md", "scripts/scan_secrets.py", "scripts/security_preflight.py", "scripts/performance_preflight.py", "scripts/record_metric.py", "scripts/metrics_report.py", "scripts/export_metrics.py", "scripts/tests/test_preflights.py", "scripts/tests/test_metrics.py",
]
REQUIRED_SKILL_HEADINGS = ("## 目标", "## 验收标准", "## 边界")
ORCHESTRATOR_REQUIRED_MARKERS = (
    "## 任务状态机",
    "DISCOVERED → SPECIFIED → PLANNED → IMPLEMENTING → VERIFIED → REVIEWED → READY_FOR_PR → RELEASED",
    "`BLOCKED`",
    "`RELEASED` 只能由人工发布流程写入",
    "`code-reviewer`",
)

def fail(message: str) -> None:
    print(f"失败：{message}", file=sys.stderr)
    raise SystemExit(1)

for relative in REQUIRED_FILES:
    if not (ROOT / relative).is_file():
        fail(f"缺少必需文件：{relative}")
orchestrator = (ROOT / ".github/agents/spring-orchestrator.agent.md").read_text(encoding="utf-8")
for marker in ORCHESTRATOR_REQUIRED_MARKERS:
    if marker not in orchestrator:
        fail(f"spring-orchestrator 缺少任务状态机标记：{marker}")
for skill in GUIDES:
    path = ROOT / ".github/skills" / skill / "SKILL.md"
    if not path.is_file():
        fail(f"缺少 Guide：{path.relative_to(ROOT)}")
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        fail(f"Guide 缺少 front matter：{path.relative_to(ROOT)}")
    for heading in REQUIRED_SKILL_HEADINGS:
        if heading not in content:
            fail(f"Guide 缺少“{heading}”：{path.relative_to(ROOT)}")
    references = list(path.parent.joinpath("references").glob("*.md"))
    if not references:
        fail(f"Guide 缺少按需加载参考：{path.relative_to(ROOT)}")
for number, line in enumerate((ROOT / ".baseline/evolution/signals.jsonl").read_text(encoding="utf-8").splitlines(), start=1):
    if line.strip():
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"第 {number} 行信号 JSON 无效：{exc}")
        if not isinstance(value, dict):
            fail(f"第 {number} 行信号不是对象")
print(f"通过：基线结构有效（{len(GUIDES)} 个 Guide、3 个 Agent、4 份专项规则）")
