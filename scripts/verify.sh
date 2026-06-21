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
  python3 scripts/record_metric.py --event-type check_run --name baseline-verify --outcome "$outcome" --duration-ms "$duration_ms" || true
  exit "$status"
}
trap record_result EXIT
python3 scripts/validate_baseline.py
python3 scripts/scan_secrets.py
python3 scripts/security_preflight.py
python3 scripts/performance_preflight.py
if [ -x ./mvnw ]; then
  ./mvnw -B -q -DskipTests verify
elif [ -f ./pom.xml ] && command -v mvn >/dev/null 2>&1; then
  mvn -B -q -DskipTests verify
elif [ -x ./gradlew ]; then
  ./gradlew --no-daemon check -x test
elif [ -f ./build.gradle ] || [ -f ./build.gradle.kts ]; then
  if command -v gradle >/dev/null 2>&1; then gradle --no-daemon check -x test; else echo "警告：检测到 Gradle，但未安装；仅完成基线结构校验" >&2; fi
else
  echo "提示：未检测到 Java 构建文件；已完成基线结构校验"
fi
