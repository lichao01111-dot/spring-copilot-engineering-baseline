# Spring 架构、事务与依赖边界手册

## 推荐依赖方向

```text
web / messaging adapter → application use case → domain
                                 ↓
                        ports / repository interfaces
                                 ↓
                    infrastructure adapters (JPA、HTTP、MQ)
```

实际项目可采用分层、模块化单体或六边形架构，但必须有一种可用 ArchUnit 或构建模块验证的依赖方向。禁止 Controller 直连 Repository；禁止领域规则散落于 DTO mapper、JPA callback 或定时任务中。

## 事务决策

| 场景 | 默认选择 | 需要额外说明 |
|---|---|---|
| 单数据库一致修改 | 单个应用服务事务 | 超时、隔离级别、锁策略 |
| 写库后发消息 | Outbox 或明确最终一致性 | 投递失败、重复、顺序、补偿 |
| 外部 HTTP 调用 | 不持有数据库事务等待远程调用 | 超时、熔断、幂等、补偿 |
| 批处理 | 小批次、可恢复 checkpoint | 事务边界、锁、吞吐、重跑 |
| 读写并发 | 乐观锁优先 | 冲突提示与重试策略 |

## 防腐与模块边界

- 外部服务返回的数据必须经适配器转换，不能让外部 DTO 污染领域模型。
- 同一业务概念在多个模块存在时，定义所有权和同步方式，不通过共享表或随意跨模块 Repository 访问解决。
- 新公共库必须保持窄接口；“方便复用”的通用 Service 往往会成为耦合点。

## ADR 最小深度

ADR 除选型外，必须记录被拒绝方案、数据与 API 兼容性、失败模式、观测指标、发布顺序和回滚/前向修复。如果这些内容无法写清，说明问题尚未被理解，不能进入开发计划。
