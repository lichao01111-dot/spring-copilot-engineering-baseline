# Spring Copilot 工程基线（中文版）

面向使用 VS Code 与 GitHub Copilot 的公司内部 Java/Spring 团队。本包将需求、设计、开发、测试、独立审查、发布准备和规则演进固化为可验证的工程流程。

设计原则：**模型负责聪明，结构负责可靠。** Guide 只说明目标、验收标准和边界；模型自主选择实现路径；编译、测试、安全扫描和审批由脚本、CI 与人工流程强制保证。

## 文档

- [总体设计](docs/DESIGN.md)
- [安装与日常使用](docs/INSTALLATION.md)
- [设计实现映射](docs/IMPLEMENTATION-MATRIX.md)

## 包含内容

- 13 个 Java/Spring Guide、3 个职责隔离 Agent、4 份路径专项规则。
- 项目画像、任务状态、演进信号、ADR/规格/计划/审查/PR/Goal 模板。
- 基线校验、构建与测试包装、密钥扫描、安全 Git Hook 和 GitHub Actions 模板。
- Java/Spring、数据库迁移、测试真实性、发布制品验证与治理标准。

## 目录结构与 Copilot 映射

```text
.
├── .github/
│   ├── copilot-instructions.md       # 所有 Copilot 请求的仓库级规则
│   ├── instructions/                 # 按文件路径自动加载：Java、测试、数据库、安全
│   ├── agents/                       # 在 VS Code Copilot Agent 下拉菜单中选择的角色
│   │   ├── spring-orchestrator       # 路由任务、维护状态、收集证据
│   │   ├── code-reviewer             # 独立两阶段审查，只读不修改
│   │   └── evolution-runner          # 度量/信号 → 规则提案，不直接生效
│   └── skills/                       # Copilot 按任务相关性加载的 13 个 Guide
│       └── <skill>/references/       # 仅复杂任务按需加载的深度手册
├── .baseline/
│   ├── project-profile.yaml          # 当前 Spring 服务的真实技术画像
│   ├── task-state/                   # 跨会话任务状态与证据
│   ├── hooks/                        # Git 门禁与会话提醒脚本
│   ├── evolution/                    # 匿名信号与待审提案
│   └── metrics/                      # Git 忽略的本地匿名度量事件
├── standards/                        # 工程、安全、性能、治理的权威标准
├── templates/                        # 规格、ADR、审查、迁移、发布和评估模板
├── scripts/                          # 构建、测试、风险扫描、度量与校验脚本
└── .github/workflows/                # GitHub Actions 质量门禁模板
```

`.github` 是 Copilot 的入口，不是普通文档目录：全局规则自动生效；路径规则随编辑文件匹配；Agent 由开发者在 Chat 下拉菜单选择；Skills 由 Agent Mode 按相关性加载或在提示中显式要求使用。

## 深度知识的加载方式

每个 Guide 保持短小，避免挤占所有任务的上下文；涉及复杂工作时，Guide 会按需加载同目录 `references/` 内的工程手册。参考手册覆盖项目发现、需求澄清、HTTP/事件契约、Spring 分层与事务、Phase 规划、JPA/测试矩阵、迁移发布、证据排障、两阶段审查、制品发布和规则治理。

Java 代码可读性采用“可读规则 + 自动 formatter + 语义审查”的组合，详见 [Java/Spring 可读性与实战编码规范](standards/java-readability-and-conventions.md) 与 [构建工具接入策略](standards/java-tooling-integration.md)。

多微服务协作采用“workspace 服务地图 + 服务上下文 + 机器可读契约 + 契约测试闭环”的组合，详见 [多微服务 Workspace 与上下文工程标准](standards/multi-service-workspace.md)。这不会改变默认服务边界：同一业务聚合仍应归属一个 Spring 服务和一个 API Deployment。

安全与性能采用“风险扫描 + 评估模板 + 审查/CI 门禁”的组合，详见 [安全与性能完成门禁](standards/security-and-performance-gates.md)。

基线使用情况采用“本地匿名事件 + 聚合报告 + 显式内部导出”的组合，详见 [工程度量使用说明](docs/METRICS.md) 与 [度量与隐私治理](standards/metrics-and-privacy.md)。

## 明确不自动执行

- 推送、合并、发布、部署、生产数据修改和权限/密钥变更。
- 不可逆数据库迁移与未审批的数据回填。
- 未经过 PR 与 Code Owner 审核的新规则或新 Guide。
