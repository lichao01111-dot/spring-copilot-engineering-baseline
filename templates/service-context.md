# 服务上下文：<service-name>

> 复制到每个服务目录，推荐命名为 `SERVICE.md`。本文件服务于开发者和 AI Agent，应保持短、准、可验证。

## 服务身份

- 服务名：
- 路径：
- Deployment：
- Owner：
- 值班/告警负责人：
- 运行时：
- 构建工具：
- 默认验证命令：

## 职责边界

本服务负责：

- 

本服务不负责：

- 

禁止绕过的边界：

- 不直接读写其他服务拥有的数据表。
- 不复用其他服务的 Repository、Entity 或业务 Service。
- 跨服务通信必须通过公开 API、事件或版本化契约。

## 业务概念与不变量

| 概念 | 含义 | 关键规则 |
|---|---|---|
| AggregateRoot |  |  |
| Status |  |  |

状态机：

```text
DRAFT -> ACTIVE -> COMPLETED
      -> CANCELLED
```

关键不变量：

1. 
2. 

## 数据所有权

| 资源 | 类型 | 说明 | 是否允许外部写入 |
|---|---|---|---|
| `<table_name>` | 数据库表 |  | 否 |
| `<event_name>` | 事件 |  | 不适用 |

迁移工具：

- Flyway / Liquibase / 其他：
- migration 路径：

## 对外契约

HTTP API：

| 方法 | 路径 | 用途 | 契约文件 |
|---|---|---|---|
| POST | `/resource` |  | `openapi.yaml` |

事件/消息：

| 方向 | Topic/Queue | Schema | 兼容策略 |
|---|---|---|---|
| produce |  |  |  |
| consume |  |  |  |

错误码与兼容规则：

- 

## 依赖服务

| 依赖服务 | 调用目的 | 协议 | 超时/重试 | 降级策略 | 契约文件 |
|---|---|---|---|---|---|
|  |  | OpenAPI/Pact/Event |  |  |  |

## 本地开发与验证

启动依赖：

```sh
# mock server / docker compose / testcontainers
```

必须验证：

```sh
# 单元测试

# 集成测试

# 契约测试
```

## 常见修改路径

| 需求类型 | 需要修改 | 必须验证 |
|---|---|---|
| 新增查询字段 | Controller、DTO、OpenAPI、测试 | Web 测试、契约测试 |
| 新增状态 | 状态机、数据库约束、事件 schema、监控 | 单测、迁移测试、契约测试 |
| 调用新服务 | Client、配置、降级、契约 | mock 测试、provider verification |

## 风险与人工确认点

以下情况必须先写 ADR 或请求人工确认：

- 破坏向后兼容 API。
- 改变数据所有权。
- 新增跨服务同步调用链。
- 新增不可逆 migration。
- 改变 Deployment、SLO、认证授权边界。
