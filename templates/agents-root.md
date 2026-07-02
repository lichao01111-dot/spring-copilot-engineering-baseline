# AGENTS.md

> 复制到目标 workspace 根目录并命名为 `AGENTS.md`。本文件是 AI Agent 的入口地图，只放路由规则和强约束；服务细节写在 `workspace-map.md` 与各服务 `SERVICE.md`。

## 使用方式

处理任何需求前，Agent 必须先判断任务类型：

- 单服务内部实现：读取目标服务 `SERVICE.md`，再进入对应 Guide。
- 跨服务 user story：先使用 `multi-service-discovery`。
- API/事件/DTO 变更：先使用 `api-contract-builder`，再使用 `contract-test-builder`。
- 服务拆分、数据所有权变化、Deployment 变化：先使用 `spring-architecture` 并生成 ADR。

## 必读入口

1. `workspace-map.md`
2. 相关服务的 `SERVICE.md`
3. 相关 OpenAPI/Pact/AsyncAPI/Proto/schema
4. `.github/copilot-instructions.md`
5. `.baseline/project-profile.yaml`

## 服务路由

| 需求关键词/业务能力 | 首选服务 | 必读文件 |
|---|---|---|
| 订单创建、取消、查询 | `services/order-service` | `services/order-service/SERVICE.md` |
| 支付、退款、回调 | `services/payment-service` | `services/payment-service/SERVICE.md` |
| 库存锁定、释放、扣减 | `services/inventory-service` | `services/inventory-service/SERVICE.md` |

## 强约束

1. 不允许按 CRUD、Controller、表或页面随意拆服务。
2. 不允许跨服务直接读写数据库。
3. 不允许共享 JPA Entity、Repository、Mapper 或业务 Service。
4. 修改服务间协议前，先更新机器可读契约。
5. 没有契约验证证据时，不得声称跨服务变更已完成。
6. 生产发布、权限、密钥、不可逆 migration 必须人工批准。

## 跨服务任务输出要求

Agent 必须在计划中列出：

- 直接修改服务。
- 只需要契约验证的服务。
- OpenAPI/Pact/事件 schema 影响。
- 数据所有权影响。
- Deployment/SLO/监控影响。
- 必跑验证命令。
- 需要人工确认的问题。
