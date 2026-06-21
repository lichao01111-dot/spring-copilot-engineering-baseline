#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
SIGNALS="$ROOT/.baseline/evolution/signals.jsonl"
if [ -s "$SIGNALS" ]; then
  echo "存在待处理演进信号：请使用 evolution-runner 生成可审查提案"
else
  echo "没有待处理演进信号"
fi
