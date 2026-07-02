# 在 VS Code + GitHub Copilot 中启用

## Quickstart：15 分钟跑通第一个服务

以下流程适用于一个已有的 Maven 或 Gradle Spring 服务。先在该服务中创建独立分支；不要直接覆盖已有 `.github/` 规则。

```sh
# 1. 在目标 Spring 服务根目录创建接入分支
git switch -c chore/add-copilot-engineering-baseline

# 2. 克隆基线到临时目录
git clone https://github.com/lichao01111-dot/spring-copilot-engineering-baseline.git /tmp/spring-copilot-baseline

# 3. 复制基线目录；若目标仓库已有 .github/，请手工合并而不是覆盖
cp -R /tmp/spring-copilot-baseline/.baseline .
cp -R /tmp/spring-copilot-baseline/scripts .
cp -R /tmp/spring-copilot-baseline/templates .
cp -R /tmp/spring-copilot-baseline/standards .
cp -R /tmp/spring-copilot-baseline/schemas .
cp /tmp/spring-copilot-baseline/.editorconfig .
```

接着将以下内容手工合并到现有 `.github/`：`copilot-instructions.md`、`instructions/`、`agents/`、`skills/`、`workflows/` 和 `CODEOWNERS.example`。这是刻意设计的人工步骤，避免覆盖团队已有 CI、Code Owner 与 Copilot 规则。

```sh
# 4. 赋予脚本执行权限，并完成首次验证
chmod +x scripts/*.sh scripts/*.py .baseline/hooks/*
scripts/verify.sh
scripts/test.sh

# 5. 可选：安装本地 Git 门禁
scripts/install-git-hooks.sh
```

首次 `verify.sh` 在未发现构建文件时只校验基线结构；在真实 Spring 服务中会自动调用 Maven 或 Gradle。若命令失败，先修复目标项目已有构建问题，不要通过删除门禁绕过。

最后在 VS Code 打开服务根目录，确认 **Code Generation: Use Instruction Files** 已启用。在 Copilot Chat 中选择 `spring-orchestrator`，输入：

```text
使用 spring-discovery 检查当前仓库。
只更新 .baseline/project-profile.yaml；为每个关键字段列出证据路径，未知项保留 unknown。
```

成功标准：`project-profile.yaml` 已填充真实 JDK、构建/测试命令、模块、数据库/迁移工具；`scripts/verify.sh` 与 `scripts/test.sh` 可运行；Copilot Chat 的 References 中能看到 `.github/copilot-instructions.md`。

## Quickstart：多微服务 workspace

如果团队有十几个微服务，不必先把仓库物理合并。可以建立一个虚拟 monorepo：

```sh
mkdir company-workspace
cd company-workspace

# 示例：把多个服务克隆到同一本地 workspace
mkdir services
git clone git@github.com:your-org/order-service.git services/order-service
git clone git@github.com:your-org/payment-service.git services/payment-service
git clone git@github.com:your-org/inventory-service.git services/inventory-service

# 从基线复制 workspace 模板
cp /tmp/spring-copilot-baseline/templates/agents-root.md ./AGENTS.md
cp /tmp/spring-copilot-baseline/templates/workspace-map.md ./workspace-map.md
cp /tmp/spring-copilot-baseline/templates/service-context.md ./services/order-service/SERVICE.md
cp /tmp/spring-copilot-baseline/templates/service-context.md ./services/payment-service/SERVICE.md
cp /tmp/spring-copilot-baseline/templates/service-context.md ./services/inventory-service/SERVICE.md
```

然后填写 `AGENTS.md` 和 `workspace-map.md`：前者只放 Agent 路由和强约束，后者放服务路径、职责、数据所有权、Deployment、Owner、OpenAPI/Pact 位置和验证命令。每个服务的 `SERVICE.md` 只写本服务事实，不复制全局规则。

在 Copilot Chat 中处理跨服务需求时，先让 Agent 使用：

```text
使用 multi-service-discovery 分析这个 user story 的服务影响面。
先读取 workspace-map.md 和相关 SERVICE.md，不要直接改代码。
输出直接修改服务、只需契约验证服务、必跑验证命令和需要人工确认的问题。
```

如果涉及接口、事件或 DTO 变化，再继续：

```text
使用 contract-test-builder 为这次跨服务协议变化设计验证闭环。
要求列出 OpenAPI/Pact/mock/provider verification 文件位置和实际命令。
```

多服务 workspace 不改变服务拆分原则。同一业务聚合的完整生命周期仍应归属一个服务和一个 API Deployment；workspace 只是给 Agent 提供全局视图和验证闭环。

## 1. 引入基线

将 `.github/`、`.baseline/`、`scripts/`、`templates/`、`standards/` 和 `schemas/` 复制或以 Git 子模块方式引入目标 Spring 仓库。保留目标仓库原有规则；冲突由工程负责人合并，不能静默覆盖。

将 `.github/CODEOWNERS.example` 复制为 `.github/CODEOWNERS`，替换所有占位团队。VS Code/GitHub Copilot 对目录或扩展名有版本差异时，只调整加载适配层，保持 Guide、模板和脚本的职责不变。

## 2. 填写项目事实

先运行 `spring-discovery`，填写 `.baseline/project-profile.yaml`。必须确认 JDK、Spring Boot、Maven/Gradle、真实编译和测试命令、模块、迁移工具、数据库、消息组件和 CI 门禁。正式试点不得保留 `unknown`。

## 3. 接入质量门禁

```sh
chmod +x scripts/*.sh scripts/*.py .baseline/hooks/*
scripts/verify.sh
scripts/test.sh
scripts/install-git-hooks.sh
```

启用 `baseline-verify.yml`。填写真实 JDK、缓存、扫描器与测试容器后，启用 `java-quality-gate.yml`。Hook 只做校验和审查门禁，不自动推送、部署或修改远程状态。

## 4. 日常使用

1. 用 `requirements-to-spec` 写规格并创建 `.baseline/task-state/<task-id>.yaml`。
2. 用 `dev-planner` 拆 Phase；高风险变更先完成 ADR/API 契约。
3. 用 `spring-builder` 或 `bug-fixer` 实现一个变更单元。
4. 运行当前验证命令，在任务状态和 PR 中记录真实输出。
5. 用独立 `code-reviewer` 完成两阶段审查；PASS 后才可标记 `READY_FOR_PR`。

## 5. 受控演进

```sh
printf '%s' '{"skill":"code-review","outcome":"blocked","reason_code":"MISSING_ACCEPTANCE_EVIDENCE"}' | python3 scripts/record_signal.py
```

`evolution-runner` 只生成提案。任何规则变更都必须经过 PR 和 Code Owner 审核。
