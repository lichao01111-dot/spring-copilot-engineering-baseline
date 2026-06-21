# 在 VS Code + GitHub Copilot 中启用

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
