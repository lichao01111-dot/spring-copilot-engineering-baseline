#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
if [ ! -d .git ]; then echo "当前不是 Git 工作区；未安装 Hook" >&2; exit 1; fi
install -m 755 .baseline/hooks/pre-commit .git/hooks/pre-commit
install -m 755 .baseline/hooks/pre-push .git/hooks/pre-push
echo "已安装安全的 pre-commit 校验和 pre-push 审查门禁 Hook"
