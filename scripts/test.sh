#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
python3 scripts/validate_baseline.py
if [ -x ./mvnw ]; then ./mvnw -B test
elif [ -f ./pom.xml ] && command -v mvn >/dev/null 2>&1; then mvn -B test
elif [ -x ./gradlew ]; then ./gradlew --no-daemon test
elif [ -f ./build.gradle ] || [ -f ./build.gradle.kts ]; then
  if command -v gradle >/dev/null 2>&1; then gradle --no-daemon test; else echo "警告：检测到 Gradle，但未安装；仅完成基线结构校验" >&2; fi
else echo "提示：未检测到 Java 构建文件；没有可运行的应用测试"; fi
