# 多微服务 Workspace 与上下文工程标准

## 目标

当一个 user story 需要多个 Spring 微服务协作时，Agent 不能只依赖自然语言描述或临时搜索代码。它必须先获得一张稳定的服务地图，再按需加载相关服务的职责、契约、数据所有权和验证命令。

本标准用于 monorepo 或“虚拟 monorepo”。虚拟 monorepo 指多个独立仓库克隆在同一个本地目录下，由根目录的索引文件向 Agent 暴露统一视图，但不要求组织立即合并仓库。

## 推荐目录

```text
workspace-root/
├── AGENTS.md                         # Agent 全局入口与服务路由
├── workspace-map.md                  # 服务地图，来自 templates/workspace-map.md
├── services/
│   ├── order-service/
│   │   ├── SERVICE.md                # 服务上下文，来自 templates/service-context.md
│   │   ├── openapi.yaml              # 对外 HTTP 契约，如适用
│   │   └── pact/                     # Consumer-driven contract，如适用
│   ├── payment-service/
│   │   ├── SERVICE.md
│   │   ├── openapi.yaml
│   │   └── pact/
│   └── inventory-service/
│       ├── SERVICE.md
│       ├── openapi.yaml
│       └── pact/
└── shared-contracts/                 # 只放契约、schema、proto，不放共享业务实现
```

已有仓库可以不用 `services/` 目录名，但必须在 `workspace-map.md` 中写清真实路径。

## 根索引规则

根目录必须有面向 Agent 的索引。推荐文件名为 `AGENTS.md`，也可以用团队现有的 `CLAUDE.md`、`copilot-instructions.md` 或 README，但内容必须包含：

1. 服务清单与真实路径。
2. 每个服务的职责边界和数据所有权。
3. 修改某类需求时必须读取哪些服务文档。
4. 跨服务改动的禁止项和验证命令。
5. OpenAPI、Pact、AsyncAPI、Proto 或事件 schema 的位置。

根索引只做路由，不承载每个服务的全部细节。细节必须落在服务目录内，避免根文档膨胀并过期。

## 服务上下文规则

每个参与 Agent 协作的服务必须维护 `SERVICE.md` 或等价文件，至少包含：

| 内容 | 必须说明 |
|---|---|
| 职责边界 | 负责什么、不负责什么、不能绕过哪个服务 |
| 业务概念 | 聚合根、状态机、核心不变量、关键枚举 |
| 数据所有权 | 拥有哪些表、索引、迁移、事件，不允许谁直接写 |
| 对外契约 | HTTP API、事件、队列消息、错误码、兼容策略 |
| 依赖服务 | 调用原因、失败处理、超时/重试、降级 |
| 验证命令 | 单测、集成测试、契约测试、mock server 启动方式 |
| 部署边界 | Deployment、worker、CronJob、SLO、负责人 |

服务上下文不是设计愿望，而是 Agent 的工作前置条件。若文档与代码不一致，以代码、契约测试和运行验证为准，并把文档修正纳入同一 PR。

## 跨服务任务流程

跨服务任务必须经过以下步骤：

1. 读取根索引和 `workspace-map.md`。
2. 根据 user story 识别直接受影响服务和间接受影响服务。
3. 读取这些服务的 `SERVICE.md`、OpenAPI/Pact/事件 schema、数据库迁移和测试入口。
4. 生成跨服务修改计划，明确每个服务的变更、契约影响、兼容窗口和回退方式。
5. 先更新契约，再改实现；如果是兼容性破坏，必须有 ADR 和版本策略。
6. 分服务运行本地测试，再运行契约测试或 mock server 验证。
7. 输出影响面报告：服务、API、事件、数据库、配置、部署和监控。

## 与“一个聚合一个服务一个 Deployment”的关系

本标准不鼓励把同一业务聚合拆成多个微服务。它解决的是“一个需求横跨多个已经存在的服务时，Agent 如何理解协作关系”。

默认仍遵守 [服务边界与单 Deployment 规则](service-boundary-and-deployment.md)：同一业务聚合的创建、查询、修改、删除/归档、状态转换、权限、审计和数据所有权属于同一个 Spring 服务和一个 API Deployment。跨服务只能通过公开 API、事件或契约文件协作。

## 禁止项

- 不允许 Agent 通过全仓搜索后直接修改多个服务，而没有先写出受影响服务清单。
- 不允许用共享 Repository、共享 Entity 或直接连库替代服务 API。
- 不允许只改调用方代码而不更新 OpenAPI/Pact/事件 schema。
- 不允许因为端到端环境难启动就跳过契约测试；应使用 mock server 或 provider verification 替代完整环境。
- 不允许把过期手写文档作为契约依据；机器可读契约和测试优先。

## 验收标准

一个多服务 workspace 接入完成后，应满足：

1. 新人或 Agent 读取根索引后能判断“改这个需求需要看哪些服务”。
2. 每个服务能说明自己的职责、不变量、数据所有权和验证命令。
3. 至少一种机器可读契约存在：OpenAPI、Pact、AsyncAPI、Proto 或事件 schema。
4. 修改服务间接口时，契约文件、实现和测试在同一 PR 中变化。
5. CI 或本地脚本能运行基础结构校验；真实项目应再接入契约测试命令。
