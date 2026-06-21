#!/usr/bin/env sh
set -eu
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"
BASE_REF=${BASELINE_REVIEW_BASE_REF:-origin/main}
if ! git rev-parse --verify "$BASE_REF" >/dev/null 2>&1; then
  echo "审查门禁跳过：本地没有基准分支 '$BASE_REF'" >&2
  exit 0
fi
if ! git diff --quiet "$BASE_REF"...HEAD -- ':(glob)**/*.java' ':(glob)**/src/**' ':(glob)**/pom.xml' ':(glob)**/build.gradle' ':(glob)**/build.gradle.kts'; then
  if ! find .baseline/task-state -name '*.yaml' -type f -exec grep -l 'status: REVIEWED\|status: READY_FOR_PR' {} + 2>/dev/null | grep -q .; then
    echo "审查门禁失败：检测到代码变更，但没有 REVIEWED 或 READY_FOR_PR 任务状态" >&2
    exit 1
  fi
fi
