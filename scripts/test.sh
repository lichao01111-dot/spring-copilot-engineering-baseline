#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
STARTED_AT_NS=$(python3 -c 'import time; print(time.monotonic_ns())')
record_result() {
  status=$?
  trap - EXIT
  ended_at_ns=$(python3 -c 'import time; print(time.monotonic_ns())')
  duration_ms=$(( (ended_at_ns - STARTED_AT_NS) / 1000000 ))
  if [ "$status" -eq 0 ]; then outcome=passed; else outcome=failed; fi
  python3 scripts/record_metric.py --event-type check_run --name baseline-test --outcome "$outcome" --duration-ms "$duration_ms" || true
  exit "$status"
}
trap record_result EXIT
python3 scripts/validate_baseline.py
python3 -m unittest discover -s scripts/tests -p 'test_*.py'
if [ -x ./mvnw ]; then ./mvnw -B test
elif [ -f ./pom.xml ] && command -v mvn >/dev/null 2>&1; then mvn -B test
elif [ -x ./gradlew ]; then ./gradlew --no-daemon test
elif [ -f ./build.gradle ] || [ -f ./build.gradle.kts ]; then
  if command -v gradle >/dev/null 2>&1; then gradle --no-daemon test; else echo "警告：检测到 Gradle，但未安装；仅完成基线结构校验" >&2; fi
else echo "提示：未检测到 Java 构建文件；没有可运行的应用测试"; fi
